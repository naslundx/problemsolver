<template>
  <button
    class="toggler"
    @click="toggleShow"
  >
    <font-awesome-icon :icon="`fa-solid fa-circle-${icon}`" />
  </button>
</template>

<script>
export default {
  emits: ["toggle"],
  data: function () {
    return {
      show: true,
    };
  },
  computed: {
    icon: function () {
      return !this.show ? "plus" : "minus";
    },
  },
  methods: {
    toggleShow: function () {
      this.show = !this.show;
      this.$emit("toggle");
    },
  },
};
</script>

<style scoped>
.toggler {
  background: none;
  border: 0px;
  font-size: large;
  color: #345;
}

.toggler:hover {
  color: #123;
  cursor: pointer;
}
</style>
