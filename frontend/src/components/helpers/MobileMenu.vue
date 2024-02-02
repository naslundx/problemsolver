<template>
  <nav class="flexContainer">
    <div
      v-for="(item, index) in items"
      :key="index"
      :class="{
        disabled: index > numberEnabledElements,
      }"
      @click="() => scrollTo(item.target)"
    >
      <font-awesome-icon
        :icon="`fa-solid fa-${item.icon}`"
        :class="{
          blink: index == numberEnabledElements,
        }"
      />
    </div>
  </nav>
</template>

<script>
export default {
  components: {},
  props: {
    numberEnabledElements: {
      type: Number,
      default: 0,
    },
  },
  emits: ['reached'],
  data: function () {
    return {
      items: [
        {
          icon: "circle-question",
          target: "header",
          index: 0,
        },
        {
          icon: "comments",
          target: "question",
          index: 1,
        },
        {
          icon: "calculator",
          target: "notes",
          index: 2,
        },
        {
          icon: "check",
          target: "answer",
          index: 3,
        },
      ],
    };
  },
  methods: {
    scrollTo(target) {
      console.log('wtf')
      document.querySelector(`div.${target}`).scrollIntoView({
        behavior: "smooth", block: "end",
      });
      console.log(this.items.find(item => item.target === target).index);
      if (this.items.find(item => item.target === target).index === this.numberEnabledElements) {
        console.log('reached');
        this.$emit('reached');
      }
    },
  },
};
</script>

<style scoped>
.disabled {
  color: #ccc;
}

@keyframes wiggle {
  0% {
    transform: rotate(0deg) scale(100%);
    color: var(--color-text);
  }
  55% {
    transform: rotate(0deg) scale(100%);
    color: var(--color-text);
  }
  60% {
    transform: rotate(55deg) scale(200%);
    color: blue;
  }
  85% {
    transform: rotate(-55deg) scale(200%);
    color: blue;
  }
  100% {
    transform: rotate(0deg) scale(100%);
    color: var(--color-text);
  }
}

.blink {
  display: inline-block;
  animation: wiggle 3s infinite;
}

nav {
  display: flex;
  font-size: 12px;
  text-align: center;
}

.flexContainer {
  display: flex;
  flex-flow: row;
}

.flexContainer div {
  flex: 1;
  font-size: xx-large;
}

@media only screen and (min-width: 900px) {
  nav {
    display: none !important;
  }
}
</style>
