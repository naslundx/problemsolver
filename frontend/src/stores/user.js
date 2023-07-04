import { defineStore } from "pinia";
import { send } from "../assets/utils.js";

const LOCALSTORAGE_NAME = "naslundx_user";

export const useUserStore = defineStore("user", {
  state: () => ({
    game_uuid: null,
    seed: null,
    game_progress: null,
  }),
  actions: {
    clearLocalStorage() {
      localStorage.clear(LOCALSTORAGE_NAME);
    },
    saveToLocalStorage() {
      localStorage.setItem(
        LOCALSTORAGE_NAME,
        JSON.stringify({
          game_uuid: this.game_uuid,
          seed: this.seed,
          game_progress: this.game_progress,
        })
      );
    },
    async fetchGame() {
      const settings = localStorage.getItem(LOCALSTORAGE_NAME);

      if (settings) {
        const settings_json = JSON.parse(settings);
        this.game_uuid = settings_json.game_uuid;
        this.seed = settings_json.seed;
        this.game_progress = settings_json.game_progress;
        return;
      }

      const settings_json = await send("POST", "create");
      this.game_uuid = settings_json.game_uuid;
      this.seed = settings_json.seed;
      this.game_progress = settings_json.game_progress;
      this.saveToLocalStorage();
    },
    async fetchProgress() {
      const json = await send("GET", `progress?game_uuid=${this.game_uuid}`);
      this.game_progress = json.game_progress;
      this.saveToLocalStorage();
    },
  },
});
