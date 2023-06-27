import { defineStore } from "pinia";
import { send } from "../assets/utils.js";

const LOCALSTORAGE_NAME = "naslundx_user";

export const useUserStore = defineStore("user", {
  state: () => ({
    game_uuid: null,
    seed: null,
  }),
  actions: {
    async fetchGame() {
      const settings = localStorage.getItem(LOCALSTORAGE_NAME);

      if (settings) {
        const settings_json = JSON.parse(settings);
        this.game_uuid = settings_json.game_uuid;
        this.seed = settings_json.seed;
        return;
      }

      const settings_json = await send("POST", "create");
      localStorage.setItem(LOCALSTORAGE_NAME, JSON.stringify(settings_json));
      this.game_uuid = settings_json.game_uuid;
      this.seed = settings_json.seed;
    },
  },
});
