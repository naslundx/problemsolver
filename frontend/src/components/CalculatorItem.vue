<template>
  <PresentationItem
    :toggleable="true"
    :show-explanation="showExplanation"
  >
    <template #heading>
      Miniräknare
    </template>

    <div class="flexContainer">
      <div class="flexItem">
        <input
          v-model="content"
          type="text"
          placeholder="1+1"
        >
      </div>
      <span id="output">
        {{ output }}
      </span>
    </div>

    <template #explanation>
      <i>Här kan du räkna ut om du behöver.</i>
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
  data: function () {
    return {
      content: "",
    };
  },
  computed: {
    output: function () {
      const input = this.content.trim().replace(/[a-z\s]+/g, "");
      if (input.length === 0) {
        return "";
      }
      try {
        const result = eval(this.content);
        return Math.round(result * 100) / 100;
      } catch {
        return "";
      }
    },
  },
};
</script>

<style scoped>
.flexContainer {
  display: flex;
  align-items: flex-start;
  font-size: larger;
}

.flexItem {
  flex: 1;
}
</style>
