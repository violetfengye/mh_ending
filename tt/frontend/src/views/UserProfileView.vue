<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="user-info-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
              <el-button type="primary" @click="refreshUserInfo">
                刷新
              </el-button>
            </div>
          </template>

          <div class="user-info">
            <el-avatar
              :size="100"
              :src="userStore.userInfo.avatar || defaultAvatar"
            />
            <h3>{{ userStore.userInfo.username }}</h3>
            <p>{{ userStore.userInfo.email }}</p>
          </div>

          <el-divider />

          <div class="study-stats">
            <h4>学习统计</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">
                  {{ userProgress.totalQuestions || 0 }}
                </div>
                <div class="stat-label">已完成题目</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">
                  {{ userProgress.correctRate || "0%" }}
                </div>
                <div class="stat-label">正确率</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">
                  {{ userProgress.totalTime || "0h" }}
                </div>
                <div class="stat-label">学习时长</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <span>学习进度</span>
            </div>
          </template>

          <div ref="progressChart" class="progress-chart"></div>
        </el-card>

        <el-card class="history-card">
          <template #header>
            <div class="card-header">
              <span>最近练习</span>
            </div>
          </template>

          <el-table :data="practiceHistory" style="width: 100%">
            <el-table-column prop="date" label="日期" width="180" />
            <el-table-column prop="title" label="题目" />
            <el-table-column prop="score" label="得分" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.score >= 60 ? 'success' : 'danger'">
                  {{ scope.row.score }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="time" label="用时" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useUserStore } from "../stores/user";
import { getUserProgress } from "../api/math";
import { ElMessage } from "element-plus";
import * as echarts from "echarts";

const userStore = useUserStore();
const defaultAvatar =
  "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png";

const userProgress = ref({
  totalQuestions: 0,
  correctRate: "0%",
  totalTime: "0h",
});
const practiceHistory = ref([]);
const progressChart = ref<HTMLElement | null>(null);
let chart: echarts.ECharts | null = null;

onMounted(async () => {
  await loadUserProgress();
  if (progressChart.value) {
    chart = echarts.init(progressChart.value);
    renderProgressChart();
    window.addEventListener("resize", handleResize);
  }
});

onUnmounted(() => {
  if (chart) {
    chart.dispose();
  }
  window.removeEventListener("resize", handleResize);
});

async function loadUserProgress() {
  try {
    const data = await getUserProgress();
    userProgress.value = data.stats;
    practiceHistory.value = data.history;
  } catch (error) {
    ElMessage.error("加载用户进度失败");
    console.error("Failed to load user progress:", error);
  }
}

function renderProgressChart() {
  if (!chart) return;

  const option = {
    title: {
      text: "知识点掌握程度",
      left: "center",
    },
    tooltip: {
      trigger: "item",
    },
    radar: {
      indicator: [
        { name: "代数", max: 100 },
        { name: "几何", max: 100 },
        { name: "三角", max: 100 },
        { name: "微积分", max: 100 },
        { name: "概率统计", max: 100 },
      ],
    },
    series: [
      {
        name: "知识掌握度",
        type: "radar",
        data: [
          {
            value: [80, 70, 60, 50, 90],
            name: "当前水平",
          },
        ],
      },
    ],
  };

  chart.setOption(option);
}

function handleResize() {
  chart?.resize();
}

function refreshUserInfo() {
  loadUserProgress();
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.user-info-card,
.progress-card,
.history-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  text-align: center;
  padding: 20px 0;
}

.user-info h3 {
  margin: 12px 0 4px;
}

.user-info p {
  color: #909399;
  margin: 0;
}

.study-stats {
  padding: 20px 0;
}

.study-stats h4 {
  margin: 0 0 16px;
  color: #409eff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.progress-chart {
  height: 300px;
}

.history-card {
  margin-top: 20px;
}
</style>
