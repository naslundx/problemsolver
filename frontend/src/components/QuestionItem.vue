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
          v-model="content"
          class="largeFlexItem"
          @keyup.enter="onChat"
        >
        <my-button
          class="flexItem questionBtn"
          :disabled="showInfo"
          icon="comments"
          @click="onChat"
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
      <p v-visible="!!latestResponse">
        <b>Svar: </b>
        {{ latestResponse }}
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

import { mapActions, mapState } from "pinia";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    MyButton,
    LoadingAnimation,
    PresentationItem,
  },
  props: {
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  data: function () {
    return {
      content: "",
      history: [],
      isLoading: false,
    };
  },
  computed: {
    ...mapState(useQuestionStore, ["latestResponse"]),
    showInfo: function () {
      return this.content.length > 50;
    },
  },
  methods: {
    ...mapActions(useQuestionStore, ["chat"]),
    onChat: async function () {
      this.isLoading = true;
      await this.chat(this.content);
      this.isLoading = false;
    },
    clear: function () {
      this.content = "";
    },
  },
};
</script>

<style scoped>
.first {
  margin-right: 10px;
}
.flexContainer {
  display: flex;
  width: 100%;
}
.largeFlexItem {
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
