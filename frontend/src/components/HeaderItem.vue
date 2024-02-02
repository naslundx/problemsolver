<template>
  <PresentationItem
    icon="circle-question"
    class="main wrapper header"
    heading="Beskrivning"
    :show-explanation="showExplanation"
  >
    <p class="intro">
      {{ prompt }}
    </p>
    <p class="question">
      {{ question }}
    </p>

    <div class="imageContainer">
      <img
        v-if="image_url"
        :src="image_url"
      >
    </div>
    <template #explanation>
      <i>Först presenteras något som hänt och en fråga du ska svara på.</i>
    </template>
  </PresentationItem>
</template>

<script>
import PresentationItem from "./helpers/PresentationItem.vue";
import { mapActions, mapState } from "pinia";
import { useQuestionStore } from "../stores/question";

export default {
  components: {
    PresentationItem,
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
.imageContainer {
  padding: 3px;
  max-width: 70%;
  margin: 30px auto;
}
.imageContainer img {
  width: 100%;
  border-radius: 20px;
}
.intro {
}
.question {
  font-weight: bold;
}
</style>
