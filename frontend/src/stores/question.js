import { defineStore } from "pinia";
import { sleep, send } from "../assets/utils.js";

import { useUserStore } from "@/stores/user";

export const useQuestionStore = defineStore("question", {
  state: () => ({
    question_id: 0,
    question: "",
    prompt: "",
    unit: "",
    image_url: "",
    history: [],
  }),
  getters: {
    latestResponse() {
      if (this.history.length === 0) {
        return "";
      }
      return this.history[this.history.length - 1].content || "";
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
    },
    async next() {
      await this.start(this.question_id + 1);
    },
    async chat(message) {
      let userStore = useUserStore();

      const game_uuid = userStore.game_uuid;
      const seed = userStore.seed;

      this.history.push({ from: "user", content: message });

      let api = send("POST", "play", {
        action: "chat",
        question_id: this.question_id,
        question: message,
        seed,
        game_uuid,
      });

      let [_, json] = await Promise.all([sleep(3), api]);

      this.history.push({ from: "ai", content: json.response });
    },
  },
});
