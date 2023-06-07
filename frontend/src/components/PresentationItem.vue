<template>
  <div class="container">
    <div class="item">
      <h3>
        <slot name="heading" />
      </h3>

      <button 
        @click="toggleShow" 
        v-if="toggleable"
      >
        Toggle
      </button>
      
      <Transition>
        <div v-if="!toggleable || show">
          <slot />
        </div>
      </Transition>
    </div>
    <div class="explanation" v-if="showExplanation">
      <slot name="explanation"/>
    </div>
  </div>
</template>

<script>
export default {
  components: {
  },
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
    }
  },
  methods: {
    toggleShow: function () {
      this.show = !this.show;
    },
  }
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
  background-color: rgba(255,255,255,0.75);
}

.item {
  margin-left: 1rem;
  width: 67%;
}

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;
  color: var(--color-text);
}

h3 {
  font-size: 1.2rem;
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
