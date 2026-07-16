<template>
  <BasePanel
    icon="circle-question"
    class="main wrapper header"
    heading="Scenario"
    :show-explanation="showExplanation"
  >
    <div class="flexContainer">
      <div class="flexItem textContainer">
        <p class="intro">
          {{ prompt }}
        </p>
        <p class="question">
          {{ question }}
        </p>
      </div>
      <div class="flexItem imageContainer">
        <img
          v-if="image_url"
          :src="image_url"
        >
      </div>
    </div>

    <template #explanation>
      <i>Din vän har en fråga hon vill ha din hjälp med.</i>
    </template>
  </BasePanel>
</template>

<script>
import BasePanel from "./helpers/BasePanel.vue";
import { mapState } from "pinia";
import { useQuestionStore } from "../stores/question";

export default {
  components: {
    BasePanel,
  },
  props: {
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    ...mapState(useQuestionStore, ["prompt", "question", "image_url"]),
  },
};
</script>

<style scoped>
.wrapper {
  flex: 2;
  min-width: 35%;
}
button {
  margin-left: 5px;
}
.flexContainer {
  display: flex;
  flex-direction: row;
}
.flexItem {
  flex: 1;
}
.textContainer {
  padding: 10px;
}
.textContainer p {
  margin-top: 10px;
}
.imageContainer {
  padding-left: 10px;
  max-width: 50%;
  max-height: 30%;
}
.imageContainer img {
  width: 100%;
  mask-image: linear-gradient(to right, transparent 0%, black 10%);
  mask-repeat: no-repeat;
  mask-size: cover;
}
.question {
  font-weight: bold;
}

@media only screen and (min-width: 900px) {
  .intro,
  .question {
    font-size: larger;
  }
}
</style>
