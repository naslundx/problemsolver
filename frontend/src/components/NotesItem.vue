<template>
  <PresentationItem
    :toggleable="true"
    :show-explanation="true"
  >
    <template #heading>
      Anteckningar
    </template>

    <p><i>Valfria anteckningar</i></p>

    <button :disabled="true">
      Kopiera fråga & svar
    </button>

    <textarea />

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
};
</script>

<style scoped>
textarea {
  width: 100%;
  min-height: 30px;
  height: 100px;
}
</style>
