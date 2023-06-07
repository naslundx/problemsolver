<template>
  <PresentationItem :toggleable="true">
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
textarea {
  width: 100%;
  min-height: 30px;
  height: 100px;
}
</style>
