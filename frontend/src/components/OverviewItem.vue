<template>
  <PresentationItem class="main">
    <div class="container">
      <span
        v-for="number in numbersUpTo"
        :key="number"
        class="item upto"
        :class="{ selected: number - 1 == question_id }"
        @click="setQuestion(number - 1)"
      >
        {{ number }}
      </span>

      <span
        v-for="number in numbersAfter"
        :key="number"
        class="item after"
      >
        {{ number }}
      </span>
    </div>
  </PresentationItem>
</template>

<script>
import PresentationItem from "./PresentationItem.vue";
import { mapActions, mapState } from "pinia";
import { useInfoStore } from "@/stores/info";
import { useUserStore } from "@/stores/user";
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    PresentationItem,
  },
  props: {},
  computed: {
    ...mapState(useInfoStore, ["question_count"]),
    ...mapState(useUserStore, ["game_progress"]),
    ...mapState(useQuestionStore, ["question_id"]),
    numbersUpTo: function () {
      console.log(this.question_id, this.game_progress);
      const arr = Array.from(
        { length: this.game_progress + 1 },
        (_, index) => index + 1
      );
      return arr;
    },
    numbersAfter: function () {
      if (this.game_progress >= this.question_count) {
        return [];
      }
      const arr = Array.from(
        { length: this.question_count - this.game_progress - 1 },
        (_, index) => index + 1
      ).map((index) => index + this.game_progress + 1);
      return arr;
    },
  },
  methods: {
    ...mapActions(useQuestionStore, ["start"]),
    setQuestion: async function (question_id) {
      await this.start(question_id);
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
}

.item {
  margin: 0 5px;
  background-color: azure;
  padding: 0px 10px;
  border-radius: 5px;
  font-size: large;
}

.selected {
  background-color: black;
  color: white;
}

.upto {
  border: 1px solid black;
}

.upto:hover {
  background-color: black;
  color: white;
  cursor: pointer;
}

.after {
  border: 1px dashed gray;
}
</style>
