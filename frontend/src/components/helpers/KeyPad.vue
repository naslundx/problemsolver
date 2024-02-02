<template>
  <div class="buttons">
    <my-button
      text="7"
      @click="onClick('7')"
    />
    <my-button
      text="8"
      @click="onClick('8')"
    />
    <my-button
      text="9"
      @click="onClick('9')"
    />
    <my-button
      text="/"
      @click="onClick('/')"
    />
    <my-button
      text="4"
      @click="onClick('4')"
    />
    <my-button
      text="5"
      @click="onClick('5')"
    />
    <my-button
      text="6"
      @click="onClick('6')"
    />
    <my-button
      text="*"
      @click="onClick('*')"
    />
    <my-button
      text="1"
      @click="onClick('1')"
    />
    <my-button
      text="2"
      @click="onClick('2')"
    />
    <my-button
      text="3"
      @click="onClick('3')"
    />
    <my-button
      text="-"
      @click="onClick('-')"
    />
    <my-button
      text="0"
      style="flex: 2 1 10%"
      @click="onClick('0')"
    />
    <my-button
      text="C"
      @click="onClick('C')"
    />
    <my-button
      text="+"
      @click="onClick('+')"
    />
  </div>
</template>

<script>
import MyButton from "./MyButton.vue";

export default {
  components: { MyButton },
  emits: ["click"],
  methods: {
    onClick(element) {
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
