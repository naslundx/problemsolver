<template>
  <div
    class="container"
    :class="{ fullWidth: fullWidth }"
  >
    <div class="mainflexContainer">
      <div class="item">
        <h2>
          <font-awesome-icon
            v-if="!!icon"
            class="icon"
            :icon="`fa-solid fa-${icon}`"
          />
          {{ heading }}
          <!-- <toggle-button
            v-if="toggleable"
            @toggle="toggleShow"
          /> -->
          <hr v-if="!!heading">
        </h2>

        <Transition>
          <div v-if="!toggleable || show">
            <slot />
          </div>
        </Transition>
      </div>
      <div
        v-if="showExplanation && shouldShowExplanation && (!toggleable || show)"
        class="explanation"
      >
        <div class="flexcontainer">
          <span>
            <font-awesome-icon icon="fa-solid fa-circle-info" />
          </span>
          <slot name="explanation" />
          <span v-show="showOKExplanation">
            <my-button
              class="okexplanation wiggle"
              text="OK!"
              @click="OKExplanation"
            />
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MyButton from "./MyButton.vue";
import ToggleButton from "./ToggleButton.vue";

export default {
  components: {
    MyButton,
    ToggleButton,
  },
  props: {
    icon: {
      type: String,
      default: "",
    },
    heading: {
      type: String,
      default: "",
    },
    showExplanation: {
      type: Boolean,
      default: false,
    },
    toggleable: {
      type: Boolean,
      default: false,
    },
    fullWidth: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["okexplanation"],
  data: function () {
    return {
      show: true,
      shouldShowExplanation: true,
      showOKExplanation: true,
    };
  },
  methods: {
    toggleShow: function () {
      this.show = !this.show;
      this.OKExplanation();
    },
    OKExplanation: function () {
      if (this.showOKExplanation) {
        this.showOKExplanation = false;
        this.$emit("okexplanation");
      }
    },
  },
};
</script>

<style scoped>
.icon {
  margin-right: 5px;
}
.container {
  max-width: 900px;
  margin: 0px auto;
  padding: 0.75rem;
  background-color: rgba(255, 255, 255, 0.75);
}

.mainflexContainer {
  display: flex;
  gap: 10px;
}

.fullWidth {
  width: 100%;
  max-width: 100%;
}

.explanation {
  border-left: 1px dashed black;
  padding-left: 10px;
  flex: 1;
}

.explanation .flexcontainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: small;
  margin-top: 0;
}

.item {
  width: 100%;
  flex: 2;
}

h2 {
  font-size: 1.5rem;
  color: var(--color-heading);
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

hr {
  margin-bottom: 5px;
  border: 0;
  height: 1px;
  background-image: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.75),
    rgba(0, 0, 0, 0)
  );
}

.okexplanation {
  margin-top: 10px;
  padding: 10px;
  font-size: larger;
  border: 1px solid black;
}

@keyframes wiggle {
  0% {
    transform: rotate(0deg);
    background-color: white;
  }
  75% {
    transform: rotate(0deg);
    background-color: white;
  }
  80% {
    transform: rotate(15deg);
    background-color: orange;
  }
  95% {
    transform: rotate(-15deg);
    background-color: orange;
  }
  100% {
    transform: rotate(0deg);
    background-color: white;
  }
}

.wiggle {
  display: inline-block;
  animation: wiggle 2s infinite;
}

.wiggle:hover {
  animation: none;
}

@media only screen and (max-width: 800px) {
  .mainflexContainer {
    flex-direction: column;
    height: 100%;
  }
  .explanation {
    border-left: 0;
    border-top: 1px dashed black;
  }
}
</style>
