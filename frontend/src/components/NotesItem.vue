<template>
  <PresentationItem
    class="wrapper notes"
    icon="note-sticky"
    heading="Anteckningar & Miniräknare"
    :toggleable="true"
    :show-explanation="showExplanation"
  >
    <textarea 
      v-model="notes"
      placeholder="Valfria anteckningar"
    />

    <div class="calculator">
      <input
        v-model="content"
        type="text"
        placeholder="1+1"
      >
      <p id="output">
        {{ output }}
      </p>
    </div>
    <key-pad
      class="keypad"
      @click="onClick"
    />

    <template #explanation>
      <i>Här kan du spara anteckningar, samt räkna ut det du behöver i en enkel
        miniräknare.</i>
    </template>
  </PresentationItem>
</template>

<script>
import KeyPad from "./helpers/KeyPad.vue";
import PresentationItem from "./helpers/PresentationItem.vue";
import { mapState } from "pinia";
import { useUserStore } from "@/stores/user";

export default {
  components: {
    KeyPad,
    PresentationItem,
  },
  props: {
    showExplanation: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    // whenever question changes, this function will run
    game_progress() {
      this.content = "";
      this.notes = "";
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
  methods: {
    onClick(item) {
      if (item === "C") {
        this.content = "";
      } else {
        this.content += item;
      }
      document.querySelector(".calculator input").focus();
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
  height: 150px;
  font-size: larger;
  background: rgba(0, 0, 0, 0);
  border: 1px dashed gray;
  resize: none;
  border-bottom: 1px solid black;
  padding: 10px;
}

#output {
  font-weight: bold;
  font-size: 2em;
  margin-left: 10px;
  text-align: right;
  min-height: 2em;
}

input {
  font-size: xx-large;
  width: 100%;
  border: 0;
  margin-top:5px;
}

.calculator {
  width: 75%;
  margin: 0 auto;
  flex-direction: row;
  overflow-x: visible;
}

.keypad {
  width: 75%;
  margin: 10px auto;
}

.center {
  text-align: center;
}
</style>
