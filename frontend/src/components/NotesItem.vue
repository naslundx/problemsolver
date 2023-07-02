<template>
  <PresentationItem
    icon="note-sticky"
    heading="Anteckningar"
    :toggleable="true"
    :show-explanation="showExplanation"
  >
    <textarea placeholder="Valfria anteckningar" />

    <template #explanation>
      <i>Här kan du spara anteckningar om du behöver.</i>
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
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style scoped>
textarea {
  width: 100%;
  min-height: 30px;
  height: 100px;
  font-size: larger;
  background: rgba(0, 0, 0, 0);
  border: 0;
  resize: none;
}
</style>
