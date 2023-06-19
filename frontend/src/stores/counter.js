import { defineStore } from "pinia";

export const useSeedStore = defineStore("seed", {
  state: () => ({ seed: 0 }),
  actions: {
    change(value) {
      this.seed = value;
    },
  },
});
