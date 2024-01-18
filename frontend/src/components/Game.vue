<template>
  <OverviewItem
    ref="top"
    :full-width="true"
  />

  <p class="title">
    Öva problemlösning
  </p>

  <div class="sections">
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
  </div>


  <Menu/>

  <FooterItem
    ref="bottom"
    :full-width="true"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import CalculatorItem from "./CalculatorItem.vue";
import FooterItem from "./helpers/FooterItem.vue";
import HeaderItem from "./HeaderItem.vue";
import Menu from "./helpers/Menu.vue";
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
    Menu,
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
      return true; this.question_id !== 0;
    },
    showExplanation: function () {
      return false; this.question_id === 0;
    },
  },
  async mounted() {
    let result = await this.load();
    if (!result) {
      this.clearLocalStorage();
      this.load();
    }
  },
  methods: {
    ...mapActions(useInfoStore, ["fetchInfo"]),
    ...mapActions(useUserStore, ["clearLocalStorage", "fetchGame", "clear"]),
    ...mapActions(useQuestionStore, ["start"]),
    async load() {
      await Promise.all([this.fetchGame(), this.fetchInfo()]);
      return await this.start(this.game_progress);
    },
    OKExplanation: function () {
      this.item_show_index += 1;
      this.$nextTick(function () {
        const el = this.$refs.bottom.$el;
        el.scrollIntoView(false, {
          behavior: "smooth",
        });
      });
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
.sections {
  display: flex;
  flex-flow: row wrap;
  gap: 20px;
  margin: 0 20px;
}

@media only screen and (max-width: 600px) {
  .sections {
    flex-flow: row !important;    
    margin: 0;
    overflow-x: scroll;
    scroll-snap-type: x mandatory;
  }

  .sections > div {
    min-width: 100%;
    width: 100%;
    scroll-snap-align: start;
  }
}

</style>
