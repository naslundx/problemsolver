<template>
  <BasePanel
    class="wrapper answer"
    icon="check"
    heading="Svara"
    :show-explanation="showExplanation"
  >
    <div>
        <p class="">
            Lämna ditt svar här. Du får försöka flera gånger.
        </p>
      <p class="question">
        <b>{{ question }}</b>
      </p>
      <div class="wrapper">
        <div class="answerContainer">
                <input
                v-model="answer_content"
                type="number"
                @keyup.enter="answer"
                >
                <span class="units">
                {{ unit }}
                </span>
        </div>
        <div class="answerContainer">
            <FlatButton
                class="clearBtn"
                text="Rensa"
                :disabled="isLoading && answer_content.length === 0"
                icon="eraser"
                @click="clear"
            />
            <FlatButton
                :disabled="isLoading && !showAnswerButton"
                text="Svara"
                class="actionBtn"
                icon="check"
                @click="answer"
            />
        </div>
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
      <FlatButton
        v-if="answer_status === true"
        icon="chevron-right"
        class="actionBtn"
        text="Nästa fråga"
        @click="nextQuestion"
      />
    </div>

    <div
      v-if="!isLoading && !answer_status && previousAnswers.length > 0"
    >
      <p>Tidigare svar:</p>
      <p
        v-for="item of previousAnswers"
        :key="item"
      >
        {{ item }}
      </p>
    </div>

  </BasePanel>
</template>

<script>
import FlatButton from "./helpers/FlatButton.vue";
import BasePanel from "./helpers/BasePanel.vue";
import LoadingAnimation from "./helpers/LoadingAnimation.vue";

import { mapActions, mapState } from "pinia";
import { send, sleep } from "../assets/utils.js";
import { useUserStore } from "@/stores/user";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    LoadingAnimation,
    FlatButton,
    BasePanel,
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
    ...mapState(useQuestionStore, ["question_id", "unit", "question"]),
    ...mapState(useUserStore, ["game_uuid"]),
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

      let api = send("POST", "answer", {
        question_id: this.question_id,
        answer: cleanAnswer,
        game_uuid: this.game_uuid,
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

.question {
    margin-top: 30px;
    margin-bottom: 30px;
    width: fit-content;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid black;
}

.wrapper {
    width: 90%;
    max-width: 300px;
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
