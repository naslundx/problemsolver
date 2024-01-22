<template>
  <nav class="flexContainer">
    <div v-for="item in items" @click="() => scrollTo(item.target)">
     <font-awesome-icon :icon="`fa-solid fa-${item.icon}`" />
    </div>
  </nav>
</template>

<script>
export default {
  components: {},
  data: function() {
    return {
        items: [
        {
            icon: 'circle-question',
            target: 'header',
        },
        {
            icon: 'comments',
            target: 'question',
        },
        {
            icon: 'note-sticky',
            target: 'notes',
        },
        {
            icon: 'calculator',
            target: 'calculator',
        },
        {
            icon: 'check',
            target: 'answer',
        },
    ]
    };
  },
  methods: {
    scrollTo(target) {
      document.querySelector(`div.${target}`).scrollIntoView();
    },
  },
};
</script>

<style scoped>
nav {
  display: none !important;
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

@media only screen and (max-width: 800px) {
  nav {
    display: flex !important;
  }
}

</style>
