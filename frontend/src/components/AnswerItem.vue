<template>
  <PresentationItem>
    <template #heading>
      Svara
    </template>
    <p><i>Om du tror du vet svaret, skriv det här.</i></p>

    <input v-model="answer_content"> {{ answer_unit }}
    <br>
    <button @click="answer">
      Svara
    </button>
    <p>{{ answer_status }}</p>
  </PresentationItem>

  <PresentationItem v-if="answer_status">
    <button>Nästa fråga</button>
  </PresentationItem>
</template>

<script>
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
  data: function () {
    return {
      answer_content: null,
      answer_status: null,
    };
  },
  methods: {
    answer: async function () {
      this.answer_status = "";

      let json = await send("POST", "play", "chat", {
        action: "answer",
        question_id: this.question_id,
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
