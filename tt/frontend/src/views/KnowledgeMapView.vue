<template>
  <div class="knowledge-map-container">
    <el-card class="map-card">
      <template #header>
        <div class="card-header">
          <span>数学知识图谱</span>
          <el-button-group>
            <el-button type="primary" @click="refreshMap"> 刷新 </el-button>
            <el-button type="primary" @click="resetView"> 重置视图 </el-button>
          </el-button-group>
        </div>
      </template>
      <div class="content-container">
        <div ref="chartContainer" class="chart-container"></div>
        <el-drawer
          v-model="drawerVisible"
          :title="selectedNode?.name"
          direction="rtl"
          size="30%"
        >
          <div v-if="selectedNode" class="node-details">
            <h3>知识点详情</h3>
            <div class="detail-item">
              <label>类别：</label>
              <el-tag>{{ selectedNode.category }}</el-tag>
            </div>
            <div class="detail-item">
              <label>难度：</label>
              <el-tag :type="getDifficultyType(selectedNode.difficulty)">
                {{ getDifficultyText(selectedNode.difficulty) }}
              </el-tag>
            </div>
            <div class="detail-item">
              <label>内容：</label>
              <div class="content-box">
                {{ selectedNode.content }}
              </div>
            </div>
            <div class="detail-item">
              <label>相关知识点：</label>
              <div class="related-nodes">
                <el-tag
                  v-for="related in relatedNodes"
                  :key="related.id"
                  class="related-tag"
                  :type="getRelationType(related.id)"
                  @click="selectNode(related)"
                >
                  {{ related.name }}
                  <small class="relation-type">{{
                    getRelationship(related.id)
                  }}</small>
                </el-tag>
              </div>
            </div>
          </div>
        </el-drawer>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { getKnowledgeMap } from "../api/math";
import { ElMessage } from "element-plus";
import * as echarts from "echarts";

const chartContainer = ref<HTMLElement | null>(null);
let chart: echarts.ECharts | null = null;
const drawerVisible = ref(false);
const selectedNode = ref<any>(null);
const relatedNodes = ref<any[]>([]);
const graphData = ref<any>(null);

onMounted(async () => {
  if (chartContainer.value) {
    chart = echarts.init(chartContainer.value);
    await loadKnowledgeMap();
    window.addEventListener("resize", handleResize);
  }
});

onUnmounted(() => {
  if (chart) {
    chart.dispose();
  }
  window.removeEventListener("resize", handleResize);
});

function findRelatedNodes(nodeId: string) {
  if (!graphData.value) return [];

  const related = new Set<string>();
  graphData.value.links.forEach((link: any) => {
    if (link.source === nodeId) {
      related.add(link.target);
    } else if (link.target === nodeId) {
      related.add(link.source);
    }
  });

  return graphData.value.nodes.filter((node: any) => related.has(node.id));
}

function selectNode(node: any) {
  selectedNode.value = node;
  relatedNodes.value = findRelatedNodes(node.id);
  drawerVisible.value = true;
}

async function loadKnowledgeMap() {
  try {
    const data = await getKnowledgeMap();
    graphData.value = data;

    const option = {
      title: {
        text: "数学知识体系",
        top: "top",
        left: "center",
      },
      tooltip: {
        trigger: "item",
        formatter: function (params: any) {
          if (params.dataType === "node") {
            return `
              <div style="font-weight:bold">${params.data.name}</div>
              <div>类别：${params.data.category}</div>
              <div>难度：${getDifficultyText(params.data.difficulty)}</div>
            `;
          }
          return params.name;
        },
      },
      legend: {
        data: ["入门", "基础", "进阶", "高级", "专家"],
        orient: "vertical",
        left: "left",
        top: "middle",
      },
      animationDurationUpdate: 1500,
      animationEasingUpdate: "quinticInOut",
      series: [
        {
          type: "graph",
          layout: "force",
          data: data.nodes.map((node: any) => ({
            ...node,
            symbolSize: 30 + node.value * 10,
            category: node.difficulty - 1, // 使用难度作为分类
            itemStyle: {
              color: getDifficultyColor(node.difficulty),
              borderColor: "#fff",
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: "rgba(0, 0, 0, 0.3)",
            },
            label: {
              show: true,
              color: "#333",
              fontSize: 14,
            },
          })),
          links: data.links.map((link: any) => ({
            ...link,
            lineStyle: {
              color: "#666",
              width: 2,
              curveness: 0.3,
            },
          })),
          categories: [
            { name: "入门", itemStyle: { color: "#67C23A" } },
            { name: "基础", itemStyle: { color: "#909399" } },
            { name: "进阶", itemStyle: { color: "#E6A23C" } },
            { name: "高级", itemStyle: { color: "#F56C6C" } },
            { name: "专家", itemStyle: { color: "#B80000" } },
          ],
          roam: true,
          label: {
            show: true,
            position: "right",
            formatter: "{b}",
          },
          force: {
            repulsion: 200,
            edgeLength: 150,
            gravity: 0.2,
          },
          emphasis: {
            focus: "adjacency",
            lineStyle: {
              width: 4,
            },
          },
        },
      ],
    };

    chart?.setOption(option);
    chart?.on("click", function (params) {
      if (params.dataType === "node") {
        selectNode(params.data);
      }
    });
  } catch (error) {
    ElMessage.error("加载知识图谱失败");
    console.error("Failed to load knowledge map:", error);
  }
}

function handleResize() {
  chart?.resize();
}

function refreshMap() {
  loadKnowledgeMap();
}

function resetView() {
  chart?.dispatchAction({
    type: "graphRoam",
    zoom: 1,
    dx: 0,
    dy: 0,
  });
}

function getRelationType(nodeId: string) {
  if (!graphData.value) return "info";
  const link = graphData.value.links.find(
    (link: any) =>
      (link.source === selectedNode.value.id && link.target === nodeId) ||
      (link.target === selectedNode.value.id && link.source === nodeId)
  );

  switch (link?.relation_type) {
    case "包含":
      return "success";
    case "使用":
      return "warning";
    case "相关":
      return "info";
    case "扩展":
      return "danger";
    default:
      return "info";
  }
}

function getRelationship(nodeId: string) {
  if (!graphData.value) return "";
  const link = graphData.value.links.find(
    (link: any) =>
      (link.source === selectedNode.value.id && link.target === nodeId) ||
      (link.target === selectedNode.value.id && link.source === nodeId)
  );
  return link?.relation_type || "";
}

function getDifficultyType(difficulty: number) {
  switch (difficulty) {
    case 1:
      return "success"; // 入门
    case 2:
      return "info"; // 基础
    case 3:
      return "warning"; // 进阶
    case 4:
      return "danger"; // 高级
    case 5:
      return "danger"; // 专家
    default:
      return "info";
  }
}

function getDifficultyText(difficulty: number) {
  switch (difficulty) {
    case 1:
      return "入门";
    case 2:
      return "基础";
    case 3:
      return "进阶";
    case 4:
      return "高级";
    case 5:
      return "专家";
    default:
      return "未知";
  }
}

function getDifficultyColor(difficulty: number) {
  switch (difficulty) {
    case 1:
      return "#67C23A"; // 入门 - 绿色
    case 2:
      return "#909399"; // 基础 - 灰色
    case 3:
      return "#E6A23C"; // 进阶 - 橙色
    case 4:
      return "#F56C6C"; // 高级 - 红色
    case 5:
      return "#B80000"; // 专家 - 深红色
    default:
      return "#909399";
  }
}
</script>

<style scoped>
.knowledge-map-container {
  padding: 20px;
  height: calc(100vh - 40px);
}

.map-card {
  height: 100%;
}

.content-container {
  height: calc(100% - 60px);
  position: relative;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 100%;
  min-height: 500px;
}

.node-details {
  padding: 20px;
}

.detail-item {
  margin-bottom: 20px;
}

.detail-item label {
  font-weight: bold;
  color: #606266;
  margin-bottom: 8px;
  display: block;
}

.detail-item p {
  margin: 0;
  line-height: 1.6;
  color: #303133;
}

.detail-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-item li {
  margin: 8px 0;
}

.detail-item a {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}

.detail-item a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.content-box {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
  line-height: 1.6;
  color: #303133;
  margin-top: 8px;
}

.related-nodes {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.related-tag {
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
}

.related-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.relation-type {
  font-size: 12px;
  margin-top: 4px;
  opacity: 0.8;
}
</style>
