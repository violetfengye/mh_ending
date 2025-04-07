import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/knowledge-map",
      name: "knowledge-map",
      component: () => import("../views/KnowledgeMapView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/practice",
      name: "practice",
      component: () => import("../views/PracticeView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/user-profile",
      name: "user-profile",
      component: () => import("../views/UserProfileView.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  // 如果需要登录且未登录，重定向到登录页
  if (to.meta.requiresAuth && !userStore.isLoggedIn()) {
    next({ name: "login" });
  } else if (to.name === "login" && userStore.isLoggedIn()) {
    // 如果已登录且试图访问登录页，重定向到首页
    next({ name: "home" });
  } else {
    next();
  }
});

export default router;
