<template>
  <PresentationItem
    class="main"
    :show-explanation="true"
  >
    <template #heading>
      Beskrivning
    </template>
    {{ prompt }}
    <template #explanation>
      <i>Här presenteras något som hänt och en fråga du ska svara på.</i>
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
  },
};
</script>

<style scoped>
.main {
  margin-top: 30px;
}
button {
  margin-left: 5px;
}
</style>
