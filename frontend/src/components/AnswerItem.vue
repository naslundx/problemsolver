<template>
  <PresentationItem :show-explanation="showExplanation">
    <template #heading>
      Svara
    </template>

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
          {{ answerUnit }}
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
      <p v-if="clue !== ''"><b>Ledtråd: </b>{{ clue }}</p>
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

import { mapState } from 'pinia';
import { send, sleep } from "../assets/utils.js";
import { useSeedStore } from '@/stores/counter'

export default {
  components: {
    LoadingAnimation,
    MyButton,
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
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["nextQuestion"],
  data: function () {
    return {
      show: false,
      answer_content: "",
      answer_status: null,
      show_answer_button: false,
      isLoading: false,
      clue: "",
    };
  },
  computed: {
    ...mapState(useSeedStore, ['seed']),
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
    clear: function () {
      this.answer_content = "";
    },
    nextQuestion: function () {
      this.answer_content = "";
      this.answer_status = null;
      this.$emit("nextQuestion");
    },
    answer: async function () {
      this.isLoading = true;
      this.answer_status = "";

      let api = send("POST", "play", "chat", {
        action: "answer",
        question_id: this.questionId,
        answer: this.answer_content,
        seed: this.seed,
      });

      this.$nextTick(function () {
        const el = this.$refs.animation.$el;
        console.log(el);
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
