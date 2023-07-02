<template>
  <PresentationItem
    icon="check"
    heading="Svara"
    :show-explanation="showExplanation"
  >
    <div
      v-if="!isLoading"
      class="flexContainer"
    >
      <my-button
        class="clearBtn"
        :disabled="answer_content.length === 0"
        icon="eraser"
        @click="clear"
      />
      <div class="answer">
        <input
          v-model="answer_content"
          @keyup.enter="answer"
        >
        <span class="units">
          {{ unit }}
        </span>
      </div>
      <my-button
        v-if="showAnswerButton"
        class="actionBtn"
        text="Svara"
        @click="answer"
      />
    </div>
    <div
      v-if="isLoading"
      ref="animation"
    >
      <loading-animation />
    </div>
    <div
      v-if="!isLoading"
      class="result"
    >
      <p>{{ resultMessage }}</p>
      <p v-if="clue !== ''">
        <b>Ledtråd: </b>{{ clue }}
      </p>
      <my-button
        v-if="answer_status === true"
        class="actionBtn"
        text="Nästa fråga"
        @click="nextQuestion"
      />
    </div>

    <template #explanation>
      <i>
        Du svarar på den ursprungliga frågan här. Du kan försöka flera gånger.
      </i>
    </template>
  </PresentationItem>
</template>

<script>
import MyButton from "./MyButton.vue";
import PresentationItem from "./PresentationItem.vue";
import LoadingAnimation from "./LoadingAnimation.vue";

import { mapActions, mapState } from "pinia";
import { send, sleep } from "../assets/utils.js";
import { useUserStore } from "@/stores/user";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    LoadingAnimation,
    MyButton,
    PresentationItem,
  },
  props: {
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  data: function () {
    return {
      answer_content: "",
      answer_status: null,
      isLoading: false,
      clue: "",
    };
  },
  computed: {
    ...mapState(useQuestionStore, ["question_id", "unit"]),
    ...mapState(useUserStore, ["game_uuid", "seed"]),
    showAnswerButton: function () {
      return this.answer_content !== "" && this.answer_status !== true;
    },
    resultMessage: function () {
      if (this.answer_status === true) {
        return "Rätt svar!";
      }
      if (this.answer_status === false) {
        return "Tyvärr, fel svar. Svara igen. Ställ fler frågor vid behov.";
      }
      return "";
    },
  },
  methods: {
    ...mapActions(useUserStore, ["fetchProgress"]),
    ...mapActions(useQuestionStore, ["fetchNextQuestion"]),
    clear: function () {
      this.answer_content = "";
    },
    nextQuestion: async function () {
      await this.fetchProgress();
      await this.fetchNextQuestion();
      this.answer_content = "";
      this.answer_status = null;
    },
    answer: async function () {
      this.isLoading = true;
      this.answer_status = "";

      let api = send("POST", "play", {
        action: "answer",
        question_id: this.question_id,
        answer: this.answer_content,
        game_uuid: this.game_uuid,
        seed: this.seed,
      });

      this.$nextTick(function () {
        const el = this.$refs.animation.$el;
        el.scrollIntoView(true);
      });

      let [_, json] = await Promise.all([sleep(3000), api]);

      this.answer_status = json.is_correct;
      this.clue = json.clue;
      this.isLoading = false;
    },
  },
};
</script>

<style scoped>
.actionBtn {
  margin-left: 10px;
}

input {
  width: 4rem;
  font-size: x-large;
  text-align: right;
  border: 1px solid black;
  margin-right: 6px;
}

b {
  font-weight: bold;
}

.flexContainer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  align-content: flex-start;
}
.answer {
  /* border: 1px solid gray; */
  padding: 5px;
}

.result {
  margin-top: 10px;
}

.result p {
  font-size: larger;
  margin-left: 10px;
}
</style>
