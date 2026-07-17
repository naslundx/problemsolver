<template>
  <BasePanel
    class="wrapper notes"
    icon="calculator"
    heading="Miniräknare"
    :toggleable="true"
    :show-explanation="showExplanation"
  >
    <div class="calculatorArea">
      <div class="calculator">
        <p id="output">
          {{ output }}
        </p>
        <input
          v-model="content"
          type="text"
          placeholder="1+1"
        >
      </div>
      <key-pad
        class="keypad"
        @click="onClick"
      />
    </div>

    <textarea
      v-model="notes"
      placeholder="Valfria anteckningar"
    />

    <template #explanation>
      <i>Här kan du spara anteckningar, samt räkna ut det du behöver i en enkel
        miniräknare.</i>
    </template>
  </BasePanel>
</template>

<script lang="ts">
import KeyPad from "./helpers/KeyPad.vue";
import BasePanel from "./helpers/BasePanel.vue";
import { mapState } from "pinia";
import { useUserStore } from "@/stores/user";

export default {
  components: {
    KeyPad,
    BasePanel,
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
      notes: "",
    };
  },
  computed: {
    ...mapState(useUserStore, ["game_progress"]),
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
          return `= ${result < 0 ? "-" : ""}∞`;
        }

        const roundedResult = Math.round(result * 100) / 100;
        return `= ${roundedResult}`;
      } catch {
        return "";
      }
    },
  },
  watch: {
    game_progress() {
      this.content = "";
      this.notes = "";
    },
  },
  methods: {
    onClick(item: string) {
      if (item === "C") {
        this.content = "";
      } else {
        this.content += item;
      }
      const input = document.querySelector(
        ".calculator input"
      ) as HTMLInputElement;
      if (input) {
        input.focus();
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

.calculatorArea {
  margin: 0 auto;
}

textarea {
  width: 100%;
  min-height: 30px;
  height: 150px;
  font-size: larger;
  background: rgba(255, 255, 255, 0.2);
  border: 1px dashed gray;
  resize: none;
  border-top: 1px solid black;
  padding: 10px;
  font-family: "Courier new";
}

#output {
  font-weight: bold;
  font-family: "Courier new";
  font-size: 2em;
  text-align: right;
  min-height: 1.6em;
}

input {
  font-size: xx-large;
  font-family: "Courier new";
  width: 100%;
  border: 0;
  margin-top: 5px;
}

.calculator {
  width: 75%;
  margin: 0 auto;
  flex-direction: row;
  overflow-x: visible;
}

.keypad {
  width: 75%;
  max-width: 500px;
  margin: 10px auto;
}

.center {
  text-align: center;
}
</style>
