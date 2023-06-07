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

export default {
  components: {
    PresentationItem,
  },
  props: {
    questionId: {
      type: Number,
      required: true,
    },
    questionCount: {
      type: Number,
      required: true,
    },
  },
  computed: {
    numbersUpTo: function () {
      const arr = Array.from(
        { length: this.questionId + 1 },
        (_, index) => index + 1
      );
      return arr;
    },
    numbersAfter: function () {
      if (this.questionId >= this.questionCount) {
        return [];
      }
      const arr = Array.from(
        { length: this.questionCount - this.questionId - 1 },
        (_, index) => index + 1
      ).map((x) => x + this.questionId + 1);
      return arr;
    },
  },
};
</script>

<style scoped>
.main {
  margin-top: 75px;
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
