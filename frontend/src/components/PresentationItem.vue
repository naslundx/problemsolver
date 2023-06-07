<template>
  <div class="container">
    <div class="item">
      <h2>
        <slot name="heading" />
        <button
          v-if="toggleable"
          @click="toggleShow"
          class="toggler"
        >
          <font-awesome-icon icon="fa-solid fa-circle-plus" />
        </button>
      </h2>

      

      <Transition>
        <div v-if="!toggleable || show">
          <slot />
        </div>
      </Transition>
    </div>
    <div
      v-if="showExplanation"
      class="explanation"
    >
      <div>
        <span><font-awesome-icon icon="fa-solid fa-circle-info" />
          <slot name="explanation" />
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    showExplanation: {
      type: Boolean,
      default: false,
    },
    toggleable: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    return {
      show: false,
    };
  },
  methods: {
    toggleShow: function () {
      this.show = !this.show;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  border: 1px solid #ddd;
  border-radius: 8px;
  max-width: 768px;
  margin: 10px auto;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.75);
}

.explanation {
  border-left: 1px dashed black;
  padding-left: 10px;
  width: 35%;
}

.explanation div {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: small;
}

.item {
  margin-left: 1rem;
  /* padding-right: 10px; */
  width: 65%;
}

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;
  color: var(--color-text);
}

.toggler {
  background: none;
  border: 0px;
  font-size: larger;
  color:#345
}

.toggler:hover {
  background: #345;
  color: white;
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
</style>
