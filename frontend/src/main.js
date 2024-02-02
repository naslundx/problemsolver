import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCalculator,
  faCircleInfo,
  faCircleMinus,
  faCirclePlus,
  faCheck,
  faChevronRight,
  faEraser,
  faNoteSticky,
  faCircleQuestion,
  faComments,
  faPaperPlane,
} from "@fortawesome/free-solid-svg-icons";
import {} from "@fortawesome/free-solid-svg-icons";

const app = createApp(App);

app.directive("visible", function (el, binding) {
  el.style.visibility = !!binding.value ? "visible" : "hidden";
});

app.use(createPinia());
app.use(router);
app.component("FontAwesomeIcon", FontAwesomeIcon);

library.add([
  faCalculator,
  faCircleInfo,
  faCircleMinus,
  faCirclePlus,
  faCheck,
  faChevronRight,
  faEraser,
  faNoteSticky,
  faCircleQuestion,
  faComments,
  faPaperPlane,
]);

app.mount("#app");
