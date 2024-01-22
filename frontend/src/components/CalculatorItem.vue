<template>
  <PresentationItem
    class="wrapper calculator"
    icon="calculator"
    heading="Miniräknare"
    :show-explanation="showExplanation"
  >
    <div class="flexContainer">
      
    </div>

    <template #explanation>
      <i>Här kan du räkna ut om du behöver.</i>
    </template>
  </PresentationItem>
</template>

<script>
import PresentationItem from "./helpers/PresentationItem.vue"

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
  computed: {
    output: function () {
      const input = this.content
        .trim()
        .replaceAll(/\s+/g, "")
        .replaceAll(/÷/g, "/")
        .replaceAll(/(\d)\s*x\s*(\d)/g, "$1*$2")
        .replaceAll(/[a-zA-Z]+/g, "");
      if (input.length === 0) {
        return "";
      }
      try {
        const result = eval(input);
        if (!isFinite(result)) {
          return `${result < 0 ? "-" : ""}∞`;
        }

        const roundedResult = Math.round(result * 100) / 100;
        return roundedResult;
      } catch {
        return "";
      }
    },
  },
};
</script>

<style scoped>
.wrapper {
  flex: 1;
}

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


</style>
