<template>
  <OverviewItem
    :question-id="question_id"
    :question-count="question_count"
  />

  <HeaderItem
    :question-id="question_id"
    :prompt="prompt"
  />

  <QuestionItem
    v-if="question_id != null"
    :question-id="question_id"
  />

  <NotesItem />

  <AnswerItem
    :question-id="question_id"
    :answer-unit="answer_unit"
    @next-question="nextQuestion"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import HeaderItem from "./HeaderItem.vue";
import NotesItem from "./NotesItem.vue";
import OverviewItem from "./OverviewItem.vue";
import QuestionItem from "./QuestionItem.vue";

import { send } from "../assets/utils.js";

export default {
  components: {
    AnswerItem,
    HeaderItem,
    NotesItem,
    OverviewItem,
    QuestionItem,
  },
  data: function () {
    return {
      content: null,
      response: null,
      prompt: "",
      answer_unit: null,
      question_id: 0,
      question_count: 0,
    };
  },
  async mounted() {
    let info = await send("GET", "info");
    this.question_count = info.question_count;
    this.changeQuestion(0);
  },
  methods: {
    changeQuestion: async function (new_question_id) {
      this.question_id = new_question_id;
      let json = await send("POST", "start", null, {
        question_id: this.question_id,
      });
      this.prompt = json.prompt;
      this.answer_unit = json.unit;
    },
    nextQuestion: function () {
      if (this.question_id < this.question_count) {
        this.changeQuestion(this.question_id + 1);
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
