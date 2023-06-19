import { defineStore } from "pinia";

export const useSeedStore = defineStore('seed', {
  state: () => ({ seed: 0 }),
  getters: {
    double: (state) => state.count * 2,
  },
  actions: {
    change(value) {
      this.seed = value;
    },
  },
})