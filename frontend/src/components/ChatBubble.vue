<template>
  <div
    class="proportional"
    :class="`bubble-align-${orientation}`"
  >
    <div :class="`bubble-${orientation}`">
      <div
        v-if="showInput"
        class="flexContainer"
      >
        <my-button
          :disabled="emptyInput"
          icon="eraser"
          class="button"
          @click="clear"
        />
        <input
          v-model="input_content"
          type="text"
          placeholder="Meddelande"
          @keyup.enter="onChat"
        >
        <my-button
          :disabled="!showInfo && emptyInput"
          icon="paper-plane"
          class="button"
          @click="onChat"
        />
      </div>
      <p v-else>
        {{ content }}
      </p>
      <p
        v-show="showInfo"
        class="info"
      >
        Frågor får max vara 75 tecken långa!
      </p>
    </div>
  </div>
</template>

<script>
import MyButton from "./MyButton.vue";

export default {
  components: {
    MyButton,
  },
  props: {
    orientation: {
      type: String,
      default: "right",
    },
    content: {
      type: String,
      default: "",
    },
    showInput: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["chat"],
  data: function () {
    return {
      input_content: "",
    };
  },
  computed: {
    emptyInput: function () {
      return this.input_content.trim().length === 0;
    },
    showInfo: function () {
      return this.showInput && this.input_content.length > 75;
    },
  },
  methods: {
    onChat: function () {
      this.$emit("chat", this.input_content);
      this.input_content = "";
    },
    clear: function () {
      this.input_content = "";
    },
  },
};
</script>

<style scoped lang="scss">
.flexContainer {
  display: flex;
  gap: 5px;
}

@media only screen and (max-width: 800px) {
  .flexContainer {
    flex-wrap: wrap;
    justify-content: flex-end;
  }
  .flexContainer .button {
    order: 9;
  }
}

input {
  background: rgba(255, 255, 255, 0.15);
  padding: 3px;
  color: white;
  width: 100%;
  font-size: large;
}

p.info {
  font-size: small !important;
  text-align: center;
  color: maroon;
}

/* --- */

@function em($value) {
  @return ($value / 16) * 1em;
}

*,
*::before,
*::after {
  margin: 0;
  border: 0;
  padding: 0;
  word-wrap: break-word;
  box-sizing: border-box;
}

body {
  font-size: 1.5em;
  margin: 1em;
}

@mixin bubble($radius: 8, $color: dodgerblue, $proportional: false) {
  $tail: $radius * 1.5;
  $half: $radius * 0.5;
  $double: $radius * 2;

  display: inline-block;
  margin: em($half);
  min-height: em($double);
  padding: em($half) em($tail);
  position: relative;
  border-radius: em($radius);
  line-height: 1.5;
  color: black;
  background-color: $color;

  @if $proportional == true {
    p {
      font-size: em($radius);
    }
  }

  &::before {
    content: "";
    display: block;
    width: em($tail);
    height: em($radius);
    position: absolute;
    right: em($radius - $tail);
    bottom: 0;
    border-left: em($radius) solid $color;
    border-bottom-left-radius: 100%;
    z-index: -1;
  }
}

@mixin bubbleFlip($radius: 8, $color: dodgerblue, $proportional: false) {
  $tail: $radius * 1.5;
  $half: $radius * 0.5;
  $double: $radius * 2;

  display: inline-block;
  margin: em($half);
  min-height: em($double);
  padding: em($half) em($tail);
  position: relative;
  border-radius: em($radius);
  line-height: 1.5;
  color: black;
  background-color: $color;

  @if $proportional == true {
    p {
      font-size: em($radius);
    }
  }

  &::before {
    content: "";
    display: block;
    width: em($tail);
    height: em($radius);
    position: absolute;
    left: em($radius - $tail);
    bottom: 0;
    border-left: em($radius) solid $color;
    border-bottom-left-radius: 100%;
    z-index: -1;
    transform: scaleX(-1);
  }
}

.bubble-align-left {
  text-align: left;
}

.bubble-align-right {
  text-align: right;
}

.proportional {
  .bubble-left {
    @include bubbleFlip(18, lightgrey, $proportional: true);
  }

  .bubble-right {
    @include bubble(18, deepskyblue, $proportional: true);
  }
}
</style>
