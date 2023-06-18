<template>
  <OverviewItem
    ref="top"
    :question-id="question_id"
    :question-count="question_count"
    :full-width="true"
  />

  <p class="title">
    Öva problemlösning
  </p>

  <HeaderItem
    :question-id="question_id"
    :prompt="prompt"
    :image-url="image_url"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <QuestionItem
    v-if="showAllItems || item_show_index > 0"
    :question-id="question_id"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <NotesItem
    v-if="showAllItems || item_show_index > 1"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <AnswerItem
    v-if="showAllItems || item_show_index > 2"
    :question-id="question_id"
    :answer-unit="answer_unit"
    :show-explanation="showExplanation"
    @next-question="nextQuestion"
    @okexplanation="OKExplanation"
  />

  <FooterItem 
    ref="bottom"
    :full-width="true"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import FooterItem from "./FooterItem.vue";
import HeaderItem from "./HeaderItem.vue";
import NotesItem from "./NotesItem.vue";
import OverviewItem from "./OverviewItem.vue";
import QuestionItem from "./QuestionItem.vue";

import { send } from "../assets/utils.js";

export default {
  components: {
    AnswerItem,
    FooterItem,
    HeaderItem,
    NotesItem,
    OverviewItem,
    QuestionItem,
  },
  data: function () {
    return {
      item_show_index: 0,
      content: null,
      response: null,
      prompt: "",
      image_url: "",
      answer_unit: null,
      question_id: 0,
      question_count: 0,
    };
  },
  computed: {
    showAllItems: function () {
      return this.question_id !== 0;
    },
    showExplanation: function () {
      return this.question_id === 0;
    },
  },
  async mounted() {
    let info = await send("GET", "info");
    this.question_count = info.question_count;
    this.changeQuestion(0);
  },
  methods: {
    OKExplanation: function () {
      this.item_show_index += 1;
      this.$nextTick(function () {
        const el = this.$refs.bottom.$el;
        el.scrollIntoView(false, {
            behavior: 'smooth',
          });
      });
    },
    changeQuestion: async function (new_question_id) {
      this.question_id = new_question_id;
      let json = await send("POST", "start", null, {
        question_id: this.question_id,
      });
      this.prompt = json.prompt;
      this.answer_unit = json.unit;
      this.image_url = json.image_url;
    },
    nextQuestion: async function () {
      if (this.question_id < this.question_count) {
        await this.changeQuestion(this.question_id + 1);
        this.$nextTick(function () {
          const el = this.$refs.top.$el;
          el.scrollIntoView({
            behavior: 'smooth',
          });
        });
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
p.title {
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 3px;
}
</style>
