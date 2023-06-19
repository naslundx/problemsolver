<template>
  <PresentationItem :show-explanation="showExplanation">
    <template #heading>
      Ställ frågor
    </template>

    <div
      v-if="!isLoading"
      class="first"
    >
      <div class="flexContainer">
        <my-button
          class="flexItem clearBtn"
          :disabled="content.length === 0"
          icon="eraser"
          @click="clear"
        />
        <input
          class="flexItem" 
          v-model="content"
          @keyup.enter="chat"
        >
        <my-button
          class="flexItem questionBtn"
          :disabled="showInfo"
          icon="comments"
          @click="chat"
        />
      </div>
      <p
        v-if="showInfo"
        class="info"
      >
        Frågor får max vara 50 tecken långa
      </p>
    </div>
    <div
      v-if="isLoading"
      class="loading"
    >
      <loading-animation />
    </div>
    <div
      v-if="!isLoading"
      class="answer"
    >
      <p v-visible="!!response">
        <b>Svar: </b>
        {{ response }}
      </p>
    </div>

    <template #explanation>
      <i>Beskrivningen innehåller inte allt du behöver veta och här kan du
        ställa klargörande frågor, till exempel "Hur många blommor har hon?".</i>
    </template>
  </PresentationItem>
</template>

<script>
import MyButton from "./MyButton.vue";
import LoadingAnimation from "./LoadingAnimation.vue";
import PresentationItem from "./PresentationItem.vue";

import { mapState } from 'pinia';
import { send, sleep } from "../assets/utils.js";
import { useSeedStore } from '@/stores/counter'

export default {
  components: {
    MyButton,
    LoadingAnimation,
    PresentationItem,
  },
  props: {
    questionId: {
      type: Number,
      required: true,
    },
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  data: function () {
    return {
      content: "",
      response: null,
      history: [],
      isLoading: false,
    };
  },
  computed: {
    ...mapState(useSeedStore, ['seed']),
    showInfo: function () {
      return this.content.length > 50;
    },
  },
  methods: {
    chat: async function () {
      this.isLoading = true;
      this.history.push({ from: "user", content: this.content });
      let api = send("POST", "play", "chat", {
        action: "chat",
        question_id: this.questionId,
        content: this.content,
        seed: this.seed,
      });
      let [_, json] = await Promise.all([sleep(3), api]);
      this.isLoading = false;
      this.history.push({ from: "ai", content: json.content });
      this.response = json.content;
    },
    clear: function () {
      this.content = "";
    },
  },
};
</script>

<style scoped>
.flexContainer {
  display: flex;
  width: 100%;
}
.flexItem {
  flex: 1;
}
input {
  font-size: x-large;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
}
.clearBtn {
  margin-right: 5px;
}
.questionBtn {
  margin-left: 5px;
}
b {
  font-weight: bold;
  text-transform: uppercase;
}
.info {
  font-size: small;
  color: maroon;
}
.answer {
  margin-top: 1rem;
}
</style>
