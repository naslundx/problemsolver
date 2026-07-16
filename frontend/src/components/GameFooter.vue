<template>
  <BasePanel>
    <div class="flexContainer">
      <span><a href="https://se.linkedin.com/in/naslundx">Marcus Näslund (c) 2025</a></span>
    </div>
  </BasePanel>
</template>

<script lang="ts">
import BasePanel from "./helpers/BasePanel.vue";

export default {
  components: {
    BasePanel,
  },
  props: {
    fullWidth: {
      type: Boolean,
      default: false,
    }
  }
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
