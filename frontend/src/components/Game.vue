<template>
  <HeaderItem 
    :questionId="question_id"
    :questionCount="question_count"
    :prompt="prompt"
  />

  <QuestionItem
    v-if="question_id != null"
    :questionId="question_id"
  />

  <NotesItem />

  <AnswerItem
    :questionId="question_id"
    :answerUnit="answer_unit"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import HeaderItem from "./HeaderItem.vue";
import NotesItem from "./NotesItem.vue";
import QuestionItem from "./QuestionItem.vue";
import PresentationItem from "./PresentationItem.vue";

import { send } from '../assets/utils.js';

export default {
  components: {
    AnswerItem,
    HeaderItem,
    NotesItem,
    PresentationItem,
    QuestionItem,
  },
  data: function () {
    return {
      content: null,
      response: null,
      prompt: '',
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
      this.changeQuestion(this.question_id + 1);
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
