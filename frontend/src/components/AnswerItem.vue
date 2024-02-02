<template>
  <PresentationItem
    class="wrapper answer"
    icon="check"
    heading="Svara"
    :show-explanation="showExplanation"
  >
    <div v-if="!isLoading">
      <p class="">
        <b>{{ question }}</b>
      </p>
      <p class="">
        Lämna ditt svar här:
      </p>
      <div class="answerContainer">
        <my-button
          class="clearBtn"
          :disabled="answer_content.length === 0"
          icon="eraser"
          @click="clear"
        />
        <div>
          <input
            v-model="answer_content"
            type="number"
            @keyup.enter="answer"
          >
          <span class="units">
            {{ unit }}
          </span>
        </div>
      </div>
      <div class="answerContainer second">
        <my-button
          :disabled="!showAnswerButton"
          text="Svara"
          class="actionBtn"
          icon="check"
          @click="answer"
        />
      </div>
    </div>
    <div
      v-if="isLoading"
      ref="animation"
    >
      <loading-animation />
    </div>
    <div
      v-else
      class="result"
    >
      <p>{{ resultMessage }}</p>
      <p v-if="clue !== ''">
        <b>Ledtråd: </b>{{ clue }}
      </p>
      <my-button
        v-if="answer_status === true"
        icon="chevron-right"
        class="actionBtn"
        text="Nästa fråga"
        @click="nextQuestion"
      />
    </div>

    <div
      v-if="!isLoading && !answer_status"
      class="flexContainer"
    >
      <p
        v-for="item of previousAnswers"
        :key="item"
      >
        {{ item }}
      </p>
    </div>

    <template #explanation>
      <i>
        Du svarar på den ursprungliga frågan här. Du kan försöka flera gånger.
      </i>
    </template>
  </PresentationItem>
</template>

<script>
import MyButton from "./helpers/MyButton.vue";
import PresentationItem from "./helpers/PresentationItem.vue";
import LoadingAnimation from "./helpers/LoadingAnimation.vue";

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
      previousAnswers: [],
    };
  },
  computed: {
    unit: function () {
      return "st";
    },
    ...mapState(useQuestionStore, ["question_id", /*"unit",*/ "question"]),
    ...mapState(useUserStore, ["game_uuid", "seed"]),
    showAnswerButton: function () {
      return this.answer_content !== "" && this.answer_status !== true;
    },
    resultMessage: function () {
      if (this.answer_status === true) {
        return "Rätt svar!";
      }
      if (this.answer_status === false) {
        return "Inte rätt. Ställ fler frågor vid behov.";
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
      window.scrollTo(0, 0);
    },
    answer: async function () {
      if (!this.answer_content) {
        return;
      }

      const cleanAnswer = this.answer_content.toString().trim();
      this.isLoading = true;
      this.answer_status = "";

      let api = send("POST", "play", {
        action: "answer",
        question_id: this.question_id,
        answer: cleanAnswer,
        game_uuid: this.game_uuid,
        seed: this.seed,
      });

      this.$nextTick(function () {
        const el = this.$refs.animation.$el;
        if (el) {
          el.scrollIntoView(true);
        }
      });

      let [_, json] = await Promise.all([sleep(3000), api]);

      this.answer_status = json.is_correct;
      this.clue = json.clue;
      if (!this.answer_status) {
        this.previousAnswers.push(cleanAnswer);
      }
      this.isLoading = false;
    },
  },
};
</script>

<style scoped>
p {
  font-size: larger;
}

.units {
  font-size: larger;
  margin-left: 5px;
}
.wrapper {
  flex: 1;
}
.answerContainer {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 10px;
  gap: 10px;
}

.answerContainer.second {
  justify-content: center;
}

input {
  width: 90%;
  font-size: x-large;
  text-align: right;
  border: 1px solid black;
}

b {
  font-weight: bold;
}

.result {
  margin-top: 30px;
}

.result p {
  font-size: larger;
}

.result button {
  margin-top: 20px;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

.hidden {
  visibility: hidden;
}

.clearBtn, .actionBtn {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
