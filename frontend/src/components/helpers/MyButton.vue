<template>
  <button :disabled="disabled">
    {{ text }}
    <font-awesome-icon
      v-if="!!icon"
      :icon="`fa-solid fa-${icon}`"
    />
  </button>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: "",
    },
    icon: {
      type: String,
      default: "",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
button {
  background-color: white;
  color: black;
  border: 2px solid #555555;
  transition-duration: 0.4s;
  font-size: large;
  padding: 6px 10px;
}
@media (hover: hover) {
  button:hover:not(:disabled) {
    background-color: #555555;
    color: white;
  }
}

button:disabled {
  opacity: 0.1;
}
</style>
