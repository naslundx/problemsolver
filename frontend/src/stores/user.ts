import { defineStore } from "pinia";
import { send } from "../assets/utils";

const LOCALSTORAGE_NAME = "naslundx_user";

export const useUserStore = defineStore("user", {
  state: () => ({
    game_uuid: null as string | null,
    game_progress: null as number | null,
  }),
  actions: {
    clearLocalStorage() {
      localStorage.removeItem(LOCALSTORAGE_NAME);
    },
    saveToLocalStorage() {
      localStorage.setItem(
        LOCALSTORAGE_NAME,
        JSON.stringify({
          game_uuid: this.game_uuid,
          game_progress: this.game_progress,
        })
      );
    },
    async fetchGame() {
      const settings = localStorage.getItem(LOCALSTORAGE_NAME);

      if (settings) {
        const settings_json = JSON.parse(settings);
        this.game_uuid = settings_json.game_uuid;
        this.game_progress = settings_json.game_progress;
        return;
      }

      const settings_json = await send("POST", "game");
      this.game_uuid = settings_json.game_uuid;
      this.game_progress = settings_json.game_progress;
      this.saveToLocalStorage();
    },
    async fetchProgress() {
      const json = await send("GET", `game?game_uuid=${this.game_uuid}`);
      this.game_progress = json.game_progress;
      this.saveToLocalStorage();
    },
  },
});
