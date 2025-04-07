import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import type { UserInfo } from "../types/api";

const TOKEN_KEY = "auth_token";
const USER_INFO_KEY = "user_info";

export const useUserStore = defineStore("user", () => {
  // 从localStorage初始化token和用户信息
  const token = ref(localStorage.getItem(TOKEN_KEY) || "");
  const userInfo = ref<UserInfo>(
    JSON.parse(localStorage.getItem(USER_INFO_KEY) || "null") || {
      username: "",
      email: "",
      profile: {
        learning_progress: {},
        practice_history: [],
        recommendations: [],
      },
    }
  );

  async function login(username: string, password: string) {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        username,
        password,
      });
      token.value = response.data.access;
      // 保存token到localStorage
      localStorage.setItem(TOKEN_KEY, token.value);
      await getUserInfo();
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  }

  async function getUserInfo() {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      userInfo.value = response.data;
      // 保存用户信息到localStorage
      localStorage.setItem(USER_INFO_KEY, JSON.stringify(userInfo.value));
    } catch (error) {
      console.error("Failed to get user info:", error);
    }
  }

  function logout() {
    token.value = "";
    userInfo.value = {
      username: "",
      email: "",
      profile: {
        learning_progress: {},
        practice_history: [],
        recommendations: [],
      },
    };
    // 清除localStorage中的数据
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_INFO_KEY);
  }

  // 检查是否已登录
  function isLoggedIn() {
    return !!token.value;
  }

  // 初始化时自动获取用户信息
  if (token.value) {
    getUserInfo();
  }

  return {
    token,
    userInfo,
    login,
    logout,
    getUserInfo,
    isLoggedIn,
  };
});
