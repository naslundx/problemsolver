<template>
  <OverviewItem
    ref="top"
    :full-width="true"
  />

  <p class="title">
    Öva problemlösning
  </p>

  <HeaderItem
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <QuestionItem
    v-if="showAllItems || item_show_index > 0"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <NotesItem
    v-if="showAllItems || item_show_index > 1"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <CalculatorItem
    v-if="showAllItems || item_show_index > 2"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <AnswerItem
    v-if="showAllItems || item_show_index > 3"
    :show-explanation="showExplanation"
    @okexplanation="OKExplanation"
  />

  <FooterItem
    ref="bottom"
    :full-width="true"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import CalculatorItem from "./CalculatorItem.vue";
import FooterItem from "./FooterItem.vue";
import HeaderItem from "./HeaderItem.vue";
import NotesItem from "./NotesItem.vue";
import OverviewItem from "./OverviewItem.vue";
import QuestionItem from "./QuestionItem.vue";

import { mapActions, mapState } from "pinia";
import { useInfoStore } from "@/stores/info";
import { useUserStore } from "@/stores/user";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    AnswerItem,
    CalculatorItem,
    FooterItem,
    HeaderItem,
    NotesItem,
    OverviewItem,
    QuestionItem,
  },
  data: function () {
    return {
      item_show_index: 0,
    };
  },
  computed: {
    ...mapState(useInfoStore, ["question_count"]),
    ...mapState(useUserStore, ["game_progress"]),
    ...mapState(useQuestionStore, ["question_id"]),
    showAllItems: function () {
      this.question_id !== 0;
    },
    showExplanation: function () {
      return this.question_id === 0;
    },
  },
  async mounted() {
    await Promise.all([this.fetchGame(), this.fetchInfo()]);
    await this.start(this.game_progress);
  },
  methods: {
    ...mapActions(useInfoStore, ["fetchInfo"]),
    ...mapActions(useUserStore, ["fetchGame"]),
    ...mapActions(useQuestionStore, ["start"]),
    OKExplanation: function () {
      this.item_show_index += 1;
      this.$nextTick(function () {
        const el = this.$refs.bottom.$el;
        el.scrollIntoView(false, {
          behavior: "smooth",
        });
      });
    },
    // nextQuestion: async function () {
    //   if (this.question_id < this.question_count) {
    //     await this.changeQuestion(this.question_id + 1);
    //     this.$nextTick(function () {
    //       const el = this.$refs.top.$el;
    //       el.scrollIntoView({
    //         behavior: "smooth",
    //       });
    //     });
    //   }
    // },
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
