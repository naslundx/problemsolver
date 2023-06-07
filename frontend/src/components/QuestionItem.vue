<template>
  <PresentationItem :show-explanation="true">
    <template #heading>
      Ställ frågor
    </template>

    <input v-model="content">
    <button @click="chat">
      Fråga
    </button>
    <p><b>Svar: </b>{{ response }}</p>

    <template #explanation>
      <i>Behöver du ställa klargörande fråga? Gör det här.</i>
    </template>
  </PresentationItem>
</template>

<script>
import PresentationItem from "./PresentationItem.vue";
import { send } from "../assets/utils.js";

export default {
  components: {
    PresentationItem,
  },
  props: {
    questionId: {
      type: Number,
      required: true,
    },
  },
  data: function () {
    return {
      content: null,
      response: null,
      history: [],
    };
  },
  methods: {
    chat: async function () {
      this.history.push({ from: "user", content: this.content });
      let json = await send("POST", "play", "chat", {
        action: "chat",
        question_id: this.questionId,
        content: this.content,
      });
      this.history.push({ from: "ai", content: json.content });
      this.response = json.content;
      console.log(this.history);
    },
  },
};
</script>

<style scoped>
input {
  width: 75%;
}
textarea {
  width: 100%;
  min-width: 100%;
}
button {
  margin-left: 5px;
}
</style>
