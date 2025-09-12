import { defineStore } from "pinia";
import { sleep, send, isEmpty } from "../assets/utils.js";

import { useUserStore } from "@/stores/user";

export const useQuestionStore = defineStore("question", {
  state: () => ({
    index: 0,
    question_id: 0,
    question: "",
    prompt: "",
    unit: "",
    image_url: "",
    history: {},
    chat: {},
    latest_chat_id: 0,
  }),
  getters: {
    currentHistory() {
      return this.history[this.latest_chat_id] || [];
    },
  },
  actions: {
    async start(id) {
      let userStore = useUserStore();

      const game_uuid = userStore.game_uuid;

      const json = await send("POST", "start", {
        question_id: id,
        game_uuid,
      });
      if (isEmpty(json)) {
        return false;
      }

      this.question_id = id;
      this.question = json.question;
      this.prompt = json.prompt;
      this.unit = json.unit;
      this.image_url = json.image_url;
      this.chat = json.chat;
      this.history = {};
      this.latest_chat_id = 0;
      return true;
    },
    async fetchNextQuestion() {
      await this.start(this.question_id + 1);
    },
    addToHistory(element) {
      this.index += 1;

      element.index = this.index;
      let history_key = element.chat_index;
      if (!(history_key in this.history)) {
        this.history[history_key] = [];
      }

      this.history[history_key].push(element);
    },
    async sendChat(message, chat_index = 0) {
      this.latest_chat_id = chat_index;
      this.addToHistory({
        from: "user",
        chat_index,
        content: message,
      });

      let userStore = useUserStore();

      const game_uuid = userStore.game_uuid;

      let api = send("POST", "chat", {
        question_id: this.question_id,
        question: message,
        chat_index,
        game_uuid,
      });

      let [_, json] = await Promise.all([sleep(3), api]);

      this.addToHistory({
        from: "ai",
        chat_index,
        content: json.response,
      });
    },
  },
});
