import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Signup from "./components/Signup.vue";
import Dashboard from "./components/Dashboard.vue";
import Home from "./components/Home.vue";
import store from "./store";

// PrimeVue CSS
import "primevue/resources/themes/saga-blue/theme.css"; // or any other theme
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

import "./assets/styles.css";

const routes = [
  { path: "/", component: Home, meta: { requiresAuth: true } },
  { path: "/login", component: Login },
  { path: "/signup", component: Signup },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    try {
      const response = await fetch("http://localhost:5000/api/user/dashboard", {
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        next();
      } else {
        next("/login");
      }
    } catch (error) {
      next("/login");
    }
  } else {
    next();
  }
});

const app = createApp(App);
app.use(PrimeVue);
app.use(store);
app.use(router);
app.mount("#app");
