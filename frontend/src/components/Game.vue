<template>
  <PresentationItem>
    <template #heading>
      Beskrivning
    </template>
    <!-- <p>Fråga {{ question_id+1 }} av {{ question_count }}</p> -->

    {{ prompt }}
  </PresentationItem>

  <QuestionItem
    v-if="question_id != null"
    :question_id="question_id"
  />

  <NotesItem />

  <AnswerItem
    :question_id="question_id"
    :answer_unit="answer_unit"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import NotesItem from "./NotesItem.vue";
import QuestionItem from "./QuestionItem.vue";
import PresentationItem from "./PresentationItem.vue";

async function send(method, url, action = null, data = null) {
  let response = await fetch(`http://localhost:5000/${url}`, {
    method,
    ...(data && { body: JSON.stringify(data) }),
  });
  let json = await response.json();
  console.log(json);
  return json;
}

export default {
  components: {
    AnswerItem,
    NotesItem,
    PresentationItem,
    QuestionItem,
  },
  data: function () {
    return {
      content: null,
      response: null,
      prompt: null,
      answer_unit: null,
      question_id: 0,
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
