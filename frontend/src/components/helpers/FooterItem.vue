<template>
  <PresentationItem>
    <div class="flexContainer">
      <span><a href="https://se.linkedin.com/in/naslundx">Marcus Näslund (c) 2023</a></span>
      <!-- <div class="vl" /> -->
    </div>
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
.flexContainer {
  display: flex;
  justify-content: center;
}
.vl {
  border-left: 3px solid black;
  margin-left: 10px;
  margin-right: 10px;
}
</style>
