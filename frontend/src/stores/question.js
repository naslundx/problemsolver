import { defineStore } from "pinia";
import { sleep, send } from "../assets/utils.js";

import { useUserStore } from "@/stores/user";

export const useQuestionStore = defineStore("question", {
  state: () => ({
    question_id: 0,
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
      return this.history[this.history - 1]?.content || "";
    },
  },
  actions: {
    async start(id) {
      console.log("start", id);
      let userStore = useUserStore();
      const seed = userStore.seed;

      let json = await send("POST", "start", null, {
        question_id: id,
        seed,
      });

      this.question_id = id;
      this.prompt = json.prompt;
      this.answer_unit = json.unit;
      this.image_url = json.image_url;
    },
    async next() {
      await this.start(this.question_id + 1);
    },
    async chat(message) {
      let userStore = useUserStore();
      const seed = userStore.seed;

      this.history.push({ from: "user", content: message });

      let api = send("POST", "play", "chat", {
        action: "chat",
        question_id: this.question_id,
        question: message,
        seed,
      });

      let [_, json] = await Promise.all([sleep(3), api]);

      // TODO $patch
      this.history.push({ from: "ai", content: json.response });
    },
  },
});
