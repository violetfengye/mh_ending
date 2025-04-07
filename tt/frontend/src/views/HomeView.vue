<template>
  <div class="home-container">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :router="true"
          class="el-menu-vertical"
          :default-active="route.path"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/knowledge-map">
            <el-icon><Share /></el-icon>
            <span>知识图谱</span>
          </el-menu-item>
          <el-menu-item index="/practice">
            <el-icon><Edit /></el-icon>
            <span>练习</span>
          </el-menu-item>
          <el-menu-item index="/user-profile">
            <el-icon><User /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header>
          <div class="header-content">
            <h2>数学学习助手</h2>
            <div class="user-info">
              <span>{{ userStore.userInfo.username }}</span>
              <el-button type="text" @click="handleLogout">退出</el-button>
            </div>
          </div>
        </el-header>

        <el-main>
          <div class="main-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="upload-card">
                  <template #header>
                    <div class="card-header">
                      <span>题目识别</span>
                    </div>
                  </template>
                  <el-upload
                    class="upload-area"
                    drag
                    action="#"
                    :auto-upload="false"
                    :on-change="handleFileChange"
                    :on-exceed="handleExceed"
                    :limit="1"
                    :file-list="fileList"
                    :before-remove="handleRemove"
                  >
                    <template v-if="!imageUrl">
                      <el-icon class="el-icon--upload"
                        ><upload-filled
                      /></el-icon>
                      <div class="el-upload__text">
                        拖拽文件到此处或 <em>点击上传</em>
                      </div>
                    </template>
                    <template v-else>
                      <div class="image-preview">
                        <img :src="imageUrl" class="preview-image" />
                      </div>
                    </template>
                  </el-upload>
                  <el-button
                    type="primary"
                    :disabled="!selectedFile"
                    @click="handleUpload"
                    style="margin-top: 16px"
                    :loading="uploading"
                  >
                    开始识别
                  </el-button>
                </el-card>
              </el-col>

              <el-col :span="12">
                <el-card class="result-card">
                  <template #header>
                    <div class="card-header">
                      <span>识别结果</span>
                    </div>
                  </template>
                  <div v-if="result" class="result-content">
                    <div class="question-section">
                      <h4>题目内容：</h4>
                      <div class="question-text">
                        <p class="main-question">{{ result.question }}</p>
                        <div class="sub-questions">
                          <div
                            v-for="item in result.sub_questions"
                            :key="item.id"
                            class="sub-question"
                          >
                            <span class="question-number">({{ item.id }})</span>
                            <span class="question-content">{{
                              item.content
                            }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="analysis-section" v-if="result.analysis">
                      <h4>解题思路：</h4>
                      <div
                        v-for="(step, index) in result.analysis"
                        :key="index"
                        class="analysis-step"
                      >
                        <h5>第{{ index }}题：</h5>
                        <p>{{ step }}</p>
                      </div>
                    </div>
                    <div class="answer-section" v-if="result.answer">
                      <h4>答案：</h4>
                      <div
                        v-for="(answer, index) in result.answer"
                        :key="index"
                        class="answer-item"
                      >
                        <span class="answer-label">第{{ index }}题：</span>
                        <span class="answer-value">{{ answer }}</span>
                      </div>
                    </div>
                  </div>
                  <el-empty v-else description="暂无识别结果" />
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import { uploadImage } from "../api/math";
import { ElMessage, ElLoading } from "element-plus";
import {
  House,
  Share,
  Edit,
  User,
  UploadFilled,
} from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const selectedFile = ref<File | null>(null);
const uploading = ref(false);
const result = ref(null);
const imageUrl = ref("");
const fileList = ref([]);

function handleFileChange(file: any) {
  selectedFile.value = file.raw;
  // 创建图片预览URL
  imageUrl.value = URL.createObjectURL(file.raw);
  fileList.value = [file];
}

function handleExceed() {
  ElMessage.warning("只能上传一张图片");
}

function handleRemove() {
  selectedFile.value = null;
  imageUrl.value = "";
  fileList.value = [];
  return true;
}

async function handleUpload() {
  if (!selectedFile.value) {
    ElMessage.warning("请先选择文件");
    return;
  }

  const loadingInstance = ElLoading.service({
    lock: true,
    text: "正在努力解析题目...",
    background: "rgba(255, 255, 255, 0.8)",
    customClass: "custom-loading",
  });

  uploading.value = true;
  try {
    const response = await uploadImage(selectedFile.value);
    result.value = response;
    ElMessage.success("识别成功");
  } catch (error) {
    console.error("上传失败:", error);
    ElMessage.error("识别失败");
  } finally {
    uploading.value = false;
    loadingInstance.close();
  }
}

async function handleLogout() {
  userStore.logout();
  router.push("/login");
  ElMessage.success("已退出登录");
}

function getQuestionFromAnalysis(analysis: string): string {
  // 从解析文本中提取题目部分
  const match = analysis.match(
    /先计算(.*?)=|将.*?得到(.*?)=|利用.*?得到(.*?)=/
  );
  if (match) {
    // 返回最后一个非空的捕获组
    for (let i = 1; i < match.length; i++) {
      if (match[i]) return match[i].trim();
    }
  }
  return analysis;
}

onMounted(() => {
  // 初始化组件
});
</script>

<style scoped>
.home-container {
  height: 100vh;
}

.el-menu-vertical {
  height: 100vh;
  border-right: none;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.main-content {
  padding: 20px;
}

.upload-card,
.result-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-area {
  width: 100%;
  :deep(.el-upload) {
    width: 100%;
  }
  :deep(.el-upload-dragger) {
    width: 100%;
  }
}

.image-preview {
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.result-content {
  padding: 16px;
}

.question-section {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #ecf5ff;
  border-radius: 4px;
}

.main-question {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
}

.sub-questions {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sub-question {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: #ffffff;
  border-radius: 4px;
  font-size: 15px;
}

.question-number {
  font-weight: bold;
  color: #409eff;
  min-width: 40px;
}

.question-content {
  color: #303133;
  font-family: "Consolas", monospace;
  letter-spacing: 1px;
  white-space: pre-wrap;
  word-break: break-all;
}

.analysis-section {
  margin-bottom: 20px;
}

h4 {
  margin-bottom: 8px;
  color: #409eff;
}

.analysis-step {
  margin-bottom: 16px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.analysis-step h5 {
  margin: 0 0 8px 0;
  color: #409eff;
}

.answer-item {
  margin-bottom: 8px;
  padding: 8px;
  background-color: #f0f9eb;
  border-radius: 4px;
}

.answer-label {
  font-weight: bold;
  color: #67c23a;
  margin-right: 8px;
}

.answer-value {
  color: #303133;
}

:deep(.custom-loading) {
  .el-loading-spinner {
    .el-loading-text {
      font-size: 16px;
      color: #409eff;
      margin-top: 10px;
    }
    .circular {
      width: 50px;
      height: 50px;
      .path {
        stroke: #409eff;
        stroke-width: 3;
      }
    }
  }
}
</style>
