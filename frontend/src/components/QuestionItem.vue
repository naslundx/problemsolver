<template>
  <PresentationItem>
    <template #heading>
      Ställ frågor
    </template>
    <p><i>Behöver du ställa klargörande fråga? Gör det här.</i></p>

    <input v-model="content">
    <br>
    <button @click="chat">
      Fråga
    </button>
    <p>{{ response }}</p>
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
  },
  data: function () {
    return {
      content: null,
      response: null,
    };
  },
  methods: {
    chat: async function () {
      let json = await send("POST", "play", "chat", {
        action: "chat",
        question_id: this.question_id,
        content: this.content,
      });
      this.response = json.content;
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
