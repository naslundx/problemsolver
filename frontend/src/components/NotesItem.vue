<template>
  <PresentationItem
    class="wrapper notes"
    icon="note-sticky"
    heading="Anteckningar & Miniräknare"
    :toggleable="true"
    :show-explanation="showExplanation"
  >
    <textarea placeholder="Valfria anteckningar" />

    <div class="calculator">
    <p>Räkna ut lite</p>
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
      <i>Här kan du spara anteckningar om du behöver.</i>
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
  data: function () {
    return {
      content: "",
    };
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
  min-width: 30%;
}

textarea {
  width: 100%;
  min-height: 30px;
  height: 100px;
  font-size: larger;
  background: rgba(0, 0, 0, 0);
  border: 0;
  resize: none;
}

#output {
  font-weight: bold;
}

input {
  font-size: larger;
}
</style>
