<template>
  <BasePanel
    class="wrapper question"
    icon="comments"
    heading="Ställ frågor"
    :show-explanation="showExplanation"
  >
    <div class="mainContainer">
      <div class="contactContainer">
        <div
          v-for="(person, index) in chat"
          :key="person.name"
          class="chat"
          :class="{ 'chat-select': index == chat_index }"
          @click="setChatIndex(index)"
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
      <i>Du behöver ta reda på mer information. I chatten kan du ställa
        frågor, till exempel "Vad kostar en glass?".</i>
    </template>
  </BasePanel>
</template>

<script>
import ChatBubble from "./helpers/ChatBubble.vue";
import LoadingAnimation from "./helpers/LoadingAnimation.vue";
import BasePanel from "./helpers/BasePanel.vue";

import { mapActions, mapState } from "pinia";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    ChatBubble,
    LoadingAnimation,
    BasePanel,
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
      chat_index: 0,
    };
  },
  computed: {
    ...mapState(useQuestionStore, ["currentHistory", "chat"]),
  },
  methods: {
    ...mapActions(useQuestionStore, ["sendChat"]),
    onChat: async function (content) {
      this.isLoading = true;
      await this.sendChat(content, this.chat_index);
      this.isLoading = false;
    },
    setChatIndex: function (index) {
      this.chat_index = index;
    },
  },
};
</script>

<style scoped>
.wrapper {
  flex: 2;
  min-width: 35%;
}

.mainContainer {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}
.contactContainer {
  display: flex;
  flex-flow: column wrap;
  gap: 5px;
  align-items: flex-start;
}
.chatContainer {
  flex-grow: 1;
}
input {
  width: 100%;
  font-size: x-large;
}
b {
  font-weight: bold;
  text-transform: uppercase;
}
.button {
    padding: 30px;
}
.answer {
  font-size: larger;
  margin-top: 1rem;
}
.chat {
  border: 2px solid rgba(0, 0, 0, 0.5);
  border-radius: 3px;
  height: 100px;
  padding: 5px;
  cursor: pointer;
  opacity: 0.5;
}
.chat-select {
  border: 2px solid rgba(0, 0, 0, 1);
  background: rgba(210, 248, 225, 1);
  opacity: 1;
}
.chat:hover {
  opacity: 1;
}
.chat p {
  text-align: center;
}
.chat img {
  max-width: 50px;
}
</style>
