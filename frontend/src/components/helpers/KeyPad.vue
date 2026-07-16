<template>
  <div class="buttons">
    <FlatButton
      text="7"
      @click="onClick('7')"
    />
    <FlatButton
      text="8"
      @click="onClick('8')"
    />
    <FlatButton
      text="9"
      @click="onClick('9')"
    />
    <FlatButton
      text="/"
      @click="onClick('/')"
    />
    <FlatButton
      text="4"
      @click="onClick('4')"
    />
    <FlatButton
      text="5"
      @click="onClick('5')"
    />
    <FlatButton
      text="6"
      @click="onClick('6')"
    />
    <FlatButton
      text="*"
      @click="onClick('*')"
    />
    <FlatButton
      text="1"
      @click="onClick('1')"
    />
    <FlatButton
      text="2"
      @click="onClick('2')"
    />
    <FlatButton
      text="3"
      @click="onClick('3')"
    />
    <FlatButton
      text="-"
      @click="onClick('-')"
    />
    <FlatButton
      text="0"
      style="flex: 2 1 10%"
      @click="onClick('0')"
    />
    <FlatButton
      text="C"
      @click="onClick('C')"
    />
    <FlatButton
      text="+"
      @click="onClick('+')"
    />
  </div>
</template>

<script lang="ts">
import FlatButton from "./FlatButton.vue";

export default {
  components: { FlatButton },
  emits: ["click"],
  methods: {
    onClick(element: string) {
      this.$emit("click", element);
    },
  },
};
</script>

<style scoped>
.buttons button {
  flex: 1;
  min-width: 20%;
}

.buttons {
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
  margin-top: 10px;
}

.explanation i {
  text-align: center;
}
</style>
