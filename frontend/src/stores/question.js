import { defineStore } from "pinia";
import { sleep, send } from "../assets/utils.js";

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
    interview: {},
    latest_interview_id: 0,
  }),
  getters: {
    currentHistory() {
      return this.history[this.latest_interview_id] || [];
    },
  },
  actions: {
    async start(id) {
      let userStore = useUserStore();

      const game_uuid = userStore.game_uuid;
      const seed = userStore.seed;

      let json = await send("POST", "start", {
        question_id: id,
        game_uuid,
        seed,
      });

      this.question_id = id;
      this.question = json.question;
      this.prompt = json.prompt;
      this.unit = json.unit;
      this.image_url = json.image_url;
      this.interview = json.interview;
    },
    async fetchNextQuestion() {
      await this.start(this.question_id + 1);
    },
    addToHistory(element) {
      this.index += 1;

      element.index = index;
      let history_key = element.interview_index;
      if (!(history_key in this.history)) {
        this.history[history_key] = [];
      }

      this.history[history_key].push(element);
    },
    async chat(message, interview_index = 0) {
      this.latest_interview_id = index;
      this.addToHistory({
        from: "user",
        interview_index,
        content: message,
      });

      let userStore = useUserStore();

      const game_uuid = userStore.game_uuid;
      const seed = userStore.seed;

      let api = send("POST", "play", {
        action: "chat",
        question_id: this.question_id,
        question: message,
        interview_index,
        seed,
        game_uuid,
      });

      let [_, json] = await Promise.all([sleep(3), api]);

      this.addToHistory({
        from: "ai",
        interview_index,
        content: json.response,
      });
    },
  },
});
