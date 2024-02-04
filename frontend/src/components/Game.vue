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

    <Transition name="fade">
      <QuestionItem
        v-if="showAllItems || item_show_index > 0"
        :show-explanation="showExplanation"
        @okexplanation="OKExplanation"
      />
    </Transition>

    <Transition name="fade">
      <NotesItem
        v-if="showAllItems || item_show_index > 1"
        :show-explanation="showExplanation"
        @okexplanation="OKExplanation"
      />
    </Transition>

    <Transition name="fade">
      <AnswerItem
        v-if="showAllItems || item_show_index > 2"
        :show-explanation="showExplanation"
        @okexplanation="OKExplanation"
      />
    </Transition>
  </div>

  <MobileMenu 
    :number-enabled-elements="item_show_index"
    @reached="onReached"
  />

  <FooterItem
    ref="bottom"
    :full-width="true"
  />
</template>

<script>
import AnswerItem from "./AnswerItem.vue";
import FooterItem from "./helpers/FooterItem.vue";
import HeaderItem from "./HeaderItem.vue";
import MobileMenu from "./helpers/MobileMenu.vue";
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
    FooterItem,
    HeaderItem,
    MobileMenu,
    NotesItem,
    OverviewItem,
    QuestionItem,
  },
  data: function () {
    return {
      item_show_index: 0,
    };
  },
  created: function () {
    if (window.innerWidth < 900) {
      this.item_show_index = 1;
    }
  },
  computed: {
    ...mapState(useInfoStore, ["question_count"]),
    ...mapState(useUserStore, ["game_progress"]),
    ...mapState(useQuestionStore, ["question_id"]),
    showAllItems: function () {
      return this.question_id !== 0;
    },
    showExplanation: function () {
      return this.question_id === 0;
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
        const el = document.querySelector('.container.wrapper:last-child') 
        console.log(el);
        el.scrollIntoView(true, {
          behavior: "smooth",
        });
      });
    },
    onReached: function () {
      this.OKExplanation();
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
  font-size: larger;
  margin-top: 5px;
  margin-bottom: 5px;
}


.sections > div {
  min-width: 100%;
  width: 100%;
  scroll-snap-align: start;
}

.sections {
    flex-grow: 1;
    flex-flow: row;
    margin: 0;
    overflow-x: scroll;
    scroll-snap-type: x mandatory;
    column-gap: 10px;
    display: flex;
  }

@media only screen and (min-width: 900px) {
  div.sections {
    flex-flow: row wrap;
    row-gap: 20px;
    column-gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
    margin-bottom: 10px;
  }

  div.sections > div {
    min-width: 40%;
    border-radius: 10px;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 1.0s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  
}
</style>
