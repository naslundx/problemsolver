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
        v-if="imageUrl"
        :src="imageUrl"
      >
    </div>
    <template #explanation>
      <i>Först presenteras något som hänt och en fråga du ska svara på.</i>
    </template>
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
    prompt: {
      type: String,
      required: true,
    },
    imageUrl: {
      type: String,
      default: "",
    },
    showExplanation: {
      type: Boolean,
      default: true,
    },
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
