<template>
  <PresentationItem>
    <template #heading>
      Anteckningar
    </template>
    <p><i>Valfria anteckningar</i></p>

    <textarea />
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
input,
textarea {
  width: 50%;
}
button {
  margin-left: 5px;
}
</style>
