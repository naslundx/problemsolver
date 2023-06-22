<template>
  <PresentationItem
    class="main"
    :show-explanation="showExplanation"
  >
    <template #heading>
      Beskrivning
    </template>
    {{ prompt }}
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
import PresentationItem from "./PresentationItem.vue";
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
    ...mapState(useQuestionStore, ["prompt", "image_url"]),
  },
};
</script>

<style scoped>
.main {
  margin-top: 5px;
}
button {
  margin-left: 5px;
}
.imageContainer {
  padding: 3px;
  margin: 3px;
  max-width: 400px;
}
.imageContainer img {
  width: 100%;
  border-radius: 10px;
}
</style>
