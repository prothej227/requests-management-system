import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RequestsView from "@/views/RequestsView.vue";
import { useUserStore } from "../stores/user";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/requests",
    name: "requests",
    component: RequestsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/stickers",
    name: "stickers",
    component: () =>
      import(/* webpackChunkName: "stickers" */ "../views/StickersView.vue"),
    meta: { requiresAuth: true },
  },

  {
    path: "/master-data/:record_name",
    name: "master-data",
    component: () =>
      import(
        /* webpackChunkName: "master-data" */ "../views/MasterRecordsView.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});
// Call checkAuth on every navigation
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  // First, if auth state is unknown (null), check it from the backend
  if (userStore.isLoggedIn === null) {
    await userStore.checkAuth();
  }

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next("/login");
  } else {
    next();
  }
});
export default router;
