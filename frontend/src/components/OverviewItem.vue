<template>
  <PresentationItem class="main">
    <div class="container">
      <span
        v-for="number in numbersUpTo"
        :key="number"
        class="item upto"
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
import { useQuestionStore } from "@/stores/question";

export default {
  components: {
    PresentationItem,
  },
  props: {},
  computed: {
    ...mapState(useInfoStore, ["question_count"]),
    ...mapState(useQuestionStore, ["question_id"]),
    numbersUpTo: function () {
      const arr = Array.from(
        { length: this.question_id + 1 },
        (_, index) => index + 1
      );
      return arr;
    },
    numbersAfter: function () {
      if (this.question_id >= this.questionCount) {
        return [];
      }
      const arr = Array.from(
        { length: this.questionCount - this.question_id - 1 },
        (_, index) => index + 1
      ).map((x) => x + this.question_id + 1);
      return arr;
    },
  },
};
</script>

<style scoped>
.main {
}

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
