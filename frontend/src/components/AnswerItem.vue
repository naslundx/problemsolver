<template>
  <PresentationItem
    :toggleable="true"
    :show-explanation="true"
  >
    <template #heading>
      Svara
    </template>
    <p><i>Om du tror du vet svaret, skriv det här.</i></p>

    <input v-model="answer_content"> {{ answerUnit }}
    <br>
    <button @click="answer">
      Svara
    </button>
    <p>{{ answer_status }}</p>
    <button
      v-if="answer_status"
      @click="nextQuestion"
    >
      Nästa fråga
    </button>

    <template #explanation>
      <i>Om du tror du vet svaret, skriv det här! Du kan försöka flera
        gånger.</i>
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
    answerUnit: {
      type: String,
      default: "",
    },
  },
  emits: ["nextQuestion"],
  data: function () {
    return {
      show: false,
      answer_content: null,
      answer_status: null,
    };
  },
  methods: {
    nextQuestion: function () {
      console.log("emitting");
      this.$emit("nextQuestion");
    },
    answer: async function () {
      this.answer_status = "";

      let json = await send("POST", "play", "chat", {
        action: "answer",
        question_id: this.questionId,
        answer: this.answer_content,
      });
      if (json.is_correct) {
        this.answer_status = "RÄTT SVAR! WOHOO";
      } else {
        this.answer_status = "Inte rätt.";
      }
    },
  },
};
</script>

<style scoped>
input,
textarea {
  width: 50%;
}
button {
  margin-left: 5px;
}
</style>
