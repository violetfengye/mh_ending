<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
import { useUserStore } from "./stores/user";
import { useRouter, useRoute } from "vue-router";
import { watch } from "vue";

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

// 路由守卫
watch(
  () => route.path,
  (path) => {
    if (!userStore.token && path !== "/login") {
      router.push("/login");
    }
  },
  { immediate: true }
);
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

#app {
  height: 100%;
}
</style>
