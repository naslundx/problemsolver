<template>
  <PresentationItem
    icon="comments"
    heading="Ställ frågor"
    :show-explanation="showExplanation"
  >
    <div class="mainContainer">
      <div class="interviewContainer">
        <div
          v-for="(person, index) in interview"
          :key="person.name"
          class="interview"
          :class="{ 'interview-select': index == interview_index }"
          @click="setInterviewIndex(index)"
        >
          <p>{{ person.name }}</p>
          <img :src="person.image">
        </div>
      </div>

      <div class="chatContainer">
        <chat-bubble
          v-for="element in currentHistory"
          :key="element.index"
          :content="element.content"
          :orientation="element.from === 'user' ? 'right' : 'left'"
        />
        <chat-bubble
          v-if="!isLoading"
          :show-input="true"
          @chat="onChat"
        />
        <loading-animation v-else />
      </div>
    </div>
    <template #explanation>
      <i>Beskrivningen innehåller inte allt du behöver veta och här kan du
        ställa klargörande frågor till någon, till exempel "Hur många blommor
        har du?".</i>
    </template>
  </PresentationItem>
</template>

<script>
import ChatBubble from "./ChatBubble.vue";
import LoadingAnimation from "./LoadingAnimation.vue";
import PresentationItem from "./PresentationItem.vue";

import { mapActions, mapState } from "pinia";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    ChatBubble,
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
      isLoading: false,
      interview_index: 0,
    };
  },
  computed: {
    ...mapState(useQuestionStore, ["currentHistory", "interview"]),
  },
  methods: {
    ...mapActions(useQuestionStore, ["chat"]),
    onChat: async function (content) {
      this.isLoading = true;
      await this.chat(content, this.interview_index);
      this.isLoading = false;
    },
    setInterviewIndex: function (index) {
      this.interview_index = index;
    },
  },
};
</script>

<style scoped>
.mainContainer {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}
.interviewContainer {
  display: flex;
  flex-flow: column wrap;
  gap: 5px;
  align-items: flex-start;
}
.chatContainer {
  flex: 1;
  border-left: 1px solid black;
  overflow-y: scroll;
}
input {
  width: 100%;
  font-size: x-large;
}
b {
  font-weight: bold;
  text-transform: uppercase;
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
@media only screen and (max-width: 800px) {
  .mainContainer {
    flex-direction: column;
  }
  .chatContainer {
    border-left: 0;
  }
}
</style>
