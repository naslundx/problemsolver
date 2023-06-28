<template>
  <PresentationItem :show-explanation="showExplanation">
    <template #heading>
      Ställ frågor
    </template>

    <div class="flexContainer">
      <div class="flexContainer">
        <div
          v-for="(person, index) in interview"
          :key="person.name"
          class="interview flexItem"
          :class="{ 'interview-select': index == interview_index }"
          @click="setInterviewIndex(index)"
        >
          <p>{{ person.name }}</p>
          <img :src="person.image">
        </div>
      </div>
      <div
        v-if="isLoading"
        class="loading"
      >
        <loading-animation />
      </div>
      <my-button
        v-if="!isLoading"
        :disabled="content.length === 0"
        icon="eraser"
        @click="clear"
      />
      <div
        v-if="!isLoading"
        class="flexItem"
      >
        <input
          v-model="content"
          @keyup.enter="onChat"
        >
      </div>
      <my-button
        v-if="!isLoading"
        :disabled="showInfo"
        icon="comments"
        @click="onChat"
      />
    </div>
    <p
      v-show="showInfo"
      class="info"
    >
      Frågor får max vara 50 tecken långa
    </p>
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
        ställa klargörande frågor till någopn, till exempel "Hur många blommor
        har du?".</i>
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
      interview_index: 0,
    };
  },
  computed: {
    ...mapState(useQuestionStore, ["latestResponse", "interview"]),
    showInfo: function () {
      return this.content.length > 50;
    },
  },
  methods: {
    ...mapActions(useQuestionStore, ["chat"]),
    onChat: async function () {
      this.isLoading = true;
      await this.chat(this.content, this.interview_index);
      this.isLoading = false;
    },
    clear: function () {
      this.content = "";
    },
    setInterviewIndex: function (index) {
      this.interview_index = index;
    },
  },
};
</script>

<style scoped>
.flexContainer {
  display: flex;
  flex-flow: center;
  gap: 5px;
  align-items: flex-start;
}
.flexItem {
  flex: 1;
}
input {
  width: 100%;
  font-size: x-large;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
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
  font-size: larger;
  margin-top: 1rem;
}
.interview {
  border: 2px solid rgba(0, 0, 0, 0.5);
  border-radius: 3px;
  height: 100px;
  padding: 5px;
  cursor: pointer;
  opacity: 0.5;
}
.interview-select {
  border: 2px solid rgba(0, 0, 0, 1);
  background: rgba(210, 248, 225, 1);
  opacity: 1;
}
.interview:hover {
  opacity: 1;
}
.interview p {
  text-align: center;
}
.interview img {
  max-width: 50px;
}
</style>
