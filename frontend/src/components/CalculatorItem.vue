<template>
  <PresentationItem
    icon="calculator"
    heading="Miniräknare"
    :show-explanation="showExplanation"
  >
    <div class="flexContainer">
      <input
        v-model="content"
        class="flexItem"
        type="text"
        placeholder="1+1"
      >
      <span>=</span>
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
        const result = eval(input);
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
  align-items: center;
  justify-content: flex-start;
  font-size: larger;
  gap: 3px;
}

.flexItem {
  flex: 1;
  max-width: 67%;
}

#output {
  font-weight: bold;
}

input {
  font-size: larger;
}
</style>
