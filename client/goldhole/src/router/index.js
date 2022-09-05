import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/offenders",
    name: "offenders",
    // route level code-splitting
    // this generates a separate chunk (src_views_OffendersView_vue.js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/OffendersView.vue"),
  },
  {
    path: "/videos",
    name: "videos",
    component: () => import("../views/VideoView.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
