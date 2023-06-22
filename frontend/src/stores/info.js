import { defineStore } from "pinia";
import { send } from "../assets/utils.js";

export const useInfoStore = defineStore("info", {
  state: () => ({ question_count: null }),
  actions: {
    async fetchInfo() {
      const json = await send("GET", "info");
      this.question_count = json.question_count;
    },
  },
});
