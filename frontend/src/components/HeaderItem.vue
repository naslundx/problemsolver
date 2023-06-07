<template>
    <PresentationItem class="main">
        <template #heading>
        Beskrivning
        </template>
        <p>Fråga {{ questionId+1 }} av {{ questionCount }}</p>

        {{ prompt }}
    </PresentationItem>
  </template>
  
  <script>
  import PresentationItem from "./PresentationItem.vue";
    
  export default {
    components: {
      PresentationItem,
    },
    props: {
      questionId: {
        type: Number,
        required: true,
      },
      questionCount: {
        type: Number,
        required: true,
      },
      prompt: {
        type: String,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .main {
    margin-top: 75px;
  }
  button {
    margin-left: 5px;
  }
  </style>
  