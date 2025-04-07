<template>
  <div class="practice-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="practice-card">
          <template #header>
            <div class="card-header">
              <span>练习题目</span>
              <el-button-group>
                <el-button type="primary" @click="getNextQuestion">
                  下一题
                </el-button>
                <el-button
                  type="success"
                  @click="submitCurrentAnswer"
                  :disabled="!currentAnswer"
                >
                  提交答案
                </el-button>
              </el-button-group>
            </div>
          </template>

          <div class="ocr-section">
            <h3>图片识别：</h3>
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleImageChange"
              :on-error="handleUploadError"
              :before-upload="beforeUpload"
              :on-success="handleSuccess"
              :on-progress="handleProgress"
              :on-exceed="handleExceed"
              :on-remove="handleRemove"
              :show-file-list="true"
              accept="image/*"
              ref="uploadRef"
            >
              <template #default>
                <el-button type="primary" @click="console.log('按钮被点击')"
                  >选择图片</el-button
                >
              </template>
              <template #tip>
                <div class="el-upload__tip">
                  支持 jpg/png 文件，且不超过 5MB
                </div>
              </template>
            </el-upload>
            <el-button
              type="success"
              @click="processImage"
              :disabled="!selectedImage"
              style="margin-left: 10px"
            >
              开始识别
            </el-button>
            <div v-if="ocrResult" class="ocr-result">
              <h4>识别结果：</h4>
              <pre class="result-text">{{ ocrResult }}</pre>
            </div>
          </div>

          <el-divider />

          <div v-if="currentQuestion" class="question-content">
            <div class="question-text">
              <h3>题目：</h3>
              <p>{{ currentQuestion.content }}</p>
            </div>

            <el-divider />

            <div class="answer-input">
              <h3>你的答案：</h3>
              <el-input
                v-model="currentAnswer"
                type="textarea"
                :rows="4"
                placeholder="请输入你的答案..."
              />
            </div>

            <div v-if="showAnswer" class="answer-analysis">
              <el-divider />
              <h3>答案解析：</h3>
              <div class="analysis-content">
                <p>{{ currentQuestion.analysis }}</p>
              </div>
            </div>
          </div>

          <el-empty v-else description="请先识别题目或选择推荐题目" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="recommendations-card">
          <template #header>
            <div class="card-header">
              <span>推荐练习</span>
              <el-button type="primary" @click="loadRecommendations">
                刷新
              </el-button>
            </div>
          </template>

          <el-scrollbar height="400px">
            <div v-if="recommendations.length" class="recommendations-list">
              <el-card
                v-for="item in recommendations"
                :key="item.id"
                class="recommendation-item"
                shadow="hover"
                @click="selectQuestion(item)"
              >
                <div class="recommendation-content">
                  <h4>{{ item.title }}</h4>
                  <p class="difficulty">
                    难度：
                    <el-rate
                      v-model="item.difficulty"
                      :max="5"
                      disabled
                      show-score
                    />
                  </p>
                </div>
              </el-card>
            </div>

            <el-empty v-else description="暂无推荐题目" />
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getRecommendations, submitAnswer, uploadImage } from "../api/math";
import { ElMessage } from "element-plus";
import type { UploadProps, UploadFile } from "element-plus";

// 直接在全局作用域测试 console.log
window.addEventListener("load", () => {
  console.log("页面加载完成");
  alert("页面加载完成");
});

console.log("脚本开始执行");
alert("脚本开始执行");

const uploadRef = ref();
const currentQuestion = ref(null);
const currentAnswer = ref("");
const showAnswer = ref(false);
const recommendations = ref([]);
const selectedImage = ref<File | null>(null);
const ocrResult = ref("");

console.log("变量初始化完成");

// 测试函数
window.testConsole = () => {
  console.log("测试console.log是否工作");
  alert("测试console.log是否工作");
};

const handleSuccess = (response: any, file: UploadFile) => {
  console.log("上传成功:", response, file);
};

const handleProgress = (event: any, file: UploadFile) => {
  console.log("上传进度:", event, file);
};

const handleExceed = (files: File[]) => {
  console.log("超出限制:", files);
};

const handleRemove = (file: UploadFile) => {
  console.log("文件移除:", file);
};

const handleImageChange = (uploadFile: UploadFile) => {
  window.testConsole(); // 调用测试函数
  alert("文件已选择");
  console.log(1);
  try {
    console.log(2);
    if (uploadFile && uploadFile.raw) {
      console.log(3);
      selectedImage.value = uploadFile.raw;
      ocrResult.value = "";
      ElMessage.success("文件已选择");
    } else {
      console.log(4);
      ElMessage.warning("无效的文件");
    }
  } catch (error) {
    console.log(5);
    console.error("处理文件改变事件时出错:", error);
  }
  console.log(6);
};

const handleUploadError = (error: Error) => {
  window.testConsole(); // 调用测试函数
  alert("上传错误");
  console.error("上传错误:", error);
};

const beforeUpload = (file: File) => {
  window.testConsole(); // 调用测试函数
  alert("开始上传前检查");
  console.log("上传前检查文件:", file);
  const isImage = file.type.startsWith("image/");
  const isLt5M = file.size / 1024 / 1024 < 5;

  if (!isImage) {
    ElMessage.error("只能上传图片文件!");
    return false;
  }
  if (!isLt5M) {
    ElMessage.error("图片大小不能超过 5MB!");
    return false;
  }
  return true;
};

async function processImage() {
  window.testConsole(); // 调用测试函数
  alert("开始处理图片");
  try {
    if (!selectedImage.value) {
      ElMessage.warning("请先选择图片");
      return;
    }

    const result = await uploadImage(selectedImage.value);
    console.log("OCR结果:", result);

    if (result && result.text) {
      ocrResult.value = result.text;
      currentQuestion.value = {
        id: Date.now(),
        title: "图片识别题目",
        content: result.text,
        analysis: "请尝试解答这道题目",
        difficulty: 1,
      };

      currentAnswer.value = "";
      showAnswer.value = false;
      ElMessage.success("识别成功");
    } else {
      ElMessage.warning("识别结果为空，请重试");
    }
  } catch (error) {
    console.error("OCR错误:", error);
    ElMessage.error("图片识别失败");
  }
}

async function loadRecommendations() {
  try {
    const data = await getRecommendations();
    recommendations.value = data;
  } catch (error) {
    console.error("加载推荐题目失败:", error);
  }
}

function selectQuestion(question: any) {
  currentQuestion.value = question;
  currentAnswer.value = "";
  showAnswer.value = false;
}

function getNextQuestion() {
  if (recommendations.value.length) {
    const nextQuestion = recommendations.value[0];
    selectQuestion(nextQuestion);
    recommendations.value = recommendations.value.slice(1);
  } else {
    ElMessage.warning("没有更多题目了");
  }
}

async function submitCurrentAnswer() {
  if (!currentQuestion.value || !currentAnswer.value) {
    ElMessage.warning("请先完成答题");
    return;
  }

  try {
    const result = await submitAnswer(
      currentQuestion.value.id,
      currentAnswer.value
    );
    ElMessage.success("提交成功");
    showAnswer.value = true;
    currentQuestion.value.analysis = result.analysis;
  } catch (error) {
    console.error("提交答案失败:", error);
    ElMessage.error("提交失败");
  }
}

onMounted(() => {
  window.testConsole(); // 调用测试函数
  console.log("组件已挂载");
  alert("组件已挂载");
  // 初始加载推荐题目
  loadRecommendations();
});
</script>

<style scoped>
.practice-container {
  padding: 20px;
}

.practice-card,
.recommendations-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-content {
  margin-top: 20px;
}

.question-text,
.answer-input,
.answer-analysis {
  margin-bottom: 20px;
}

h3 {
  margin-bottom: 12px;
  color: #409eff;
  font-size: 16px;
  font-weight: bold;
}

.ocr-section {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.ocr-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.ocr-result h4 {
  margin-bottom: 10px;
  color: #409eff;
  font-size: 14px;
}

.ocr-result p {
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 14px;
  color: #606266;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommendation-item {
  cursor: pointer;
  transition: all 0.3s;
}

.recommendation-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.recommendation-content h4 {
  margin: 0 0 8px;
  color: #303133;
}

.difficulty {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

.el-upload {
  display: inline-block;
  margin-right: 10px;
}

.el-upload__tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.answer-input .el-textarea {
  margin-top: 10px;
}

.analysis-content {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.analysis-content p {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

.result-text {
  margin: 0;
  padding: 10px;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 14px;
  color: #606266;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-family: monospace;
}
</style>
