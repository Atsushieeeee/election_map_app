<template>
  <div ref="sidebar" :class="['sidebar', { visible: show, hidden: !show }]">
    <div class="sidebar-header">{{ cityName }}</div>
    <button @click="closeSidebar" class="close-btn">×</button>
    <div class="chart-container">
      <canvas id="sidebarChart"></canvas>
    </div>
    <div class="chart-container">
      <div>{{ "人口総数:" + totalPopulation }}</div>
      <canvas id="populationChart"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, nextTick, watch } from 'vue';
import axios from 'axios';
import { Chart } from 'chart.js';
import 'chart.js/auto';

interface Vote {
  candidate_name: string;
  votes: number;
}

interface AgeGroup {
  age_group: string;
  total_population: number;
}

export default defineComponent({
  name: 'Sidebar',
  props: {
    cityName: {
      type: String,
      required: true,
    },
    show: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const sidebar = ref<HTMLDivElement | null>(null);
    const chartData = ref<Vote[]>([]);
    const ageGroupData = ref<AgeGroup[]>([]);
    const totalPopulation = ref<number | null>(null);
    let chartInstance: Chart | null = null;
    let populationChartInstance: Chart | null = null;

    const closeSidebar = () => {
      emit('update:show', false);
    };

    const parseAgeGroup = (ageGroup: string): number => {
      if (ageGroup === '100以上') return 100;
      const match = ageGroup.match(/^(\d+)-/);
      return match ? parseInt(match[1], 10) : 0;
    };

    const createCharts = () => {
      const votesChartCanvas = document.getElementById('sidebarChart') as HTMLCanvasElement;
      const populationChartCanvas = document.getElementById('populationChart') as HTMLCanvasElement;

      if (votesChartCanvas) {
        const sidebarCtx = votesChartCanvas.getContext('2d');
        if (sidebarCtx) {
          if (chartInstance) {
            chartInstance.destroy();
          }
          chartInstance = new Chart(sidebarCtx, {
            type: 'bar',
            data: {
              labels: chartData.value.map(vote => vote.candidate_name),
              datasets: [{
                label: '得票数',
                data: chartData.value.map(vote => vote.votes),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
        }
      }

      if (populationChartCanvas) {
        const populationCtx = populationChartCanvas.getContext('2d');
        if (populationCtx) {
          if (populationChartInstance) {
            populationChartInstance.destroy();
          }
          populationChartInstance = new Chart(populationCtx, {
            type: 'bar',
            data: {
              labels: ageGroupData.value
                .filter(group => group.age_group !== '総数')
                .sort((a, b) => parseAgeGroup(a.age_group) - parseAgeGroup(b.age_group))
                .map(group => group.age_group),
              datasets: [{
                label: '年齢分布',
                data: ageGroupData.value
                  .filter(group => group.age_group !== '総数')
                  .sort((a, b) => parseAgeGroup(a.age_group) - parseAgeGroup(b.age_group))
                  .map(group => group.total_population),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
        }
      }
    };

    watch(() => props.show, async (newValue: boolean) => {
      if (newValue) {
        await fetchData(props.cityName);
        nextTick(() => {
          createCharts();
        });
      }
    });

    watch(() => props.cityName, async (newValue: string) => {
      if (props.show) {
        await fetchData(newValue);
        nextTick(() => {
          createCharts();
        });
      }
    });

    const fetchData = async (cityName: string) => {
      try {
        const votesResponse = await axios.get<Vote[]>('http://127.0.0.1:8000/api/votes/', {
          params: {
            city: cityName,
            election_date: '2024-07-07',
            region: '東京都'
          }
        });
        chartData.value = votesResponse.data.sort((a, b) => b.votes - a.votes).slice(0, 10);

        const populationResponse = await axios.get('http://127.0.0.1:8000/api/population_distribution/', {
          params: {
            region: cityName
          }
        });

        const populationData = populationResponse.data;
        ageGroupData.value = populationData.age_groups;
        totalPopulation.value = populationData.total_population;
      } catch (error) {
        console.error('データの読み込みに失敗しました', error);
      }
    };

    return { sidebar, closeSidebar, totalPopulation };
  }
});
</script>

<style scoped>
.sidebar {
  position: fixed;
  right: 0;
  top: 0;
  width: 600px;
  height: 100%;
  background: #fff;
  border-left: 1px solid #ddd;
  box-shadow: -2px 0 5px rgba(0,0,0,0.3);
  padding: 20px;
  z-index: 1000;
  overflow-y: auto;
  transform: translateX(100%); /* 初期状態で右外 */
  opacity: 0; /* 初期状態で非表示 */
  transition: transform 0.3s ease, opacity 0.3s ease; /* スライドとフェードのアニメーション */
}

.sidebar.visible {
  transform: translateX(0); /* 表示状態 */
  opacity: 1; /* 表示状態 */
}

.sidebar.hidden {
  transform: translateX(100%); /* 非表示状態 */
  opacity: 0; /* 非表示状態 */
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}

.chart-container {
  margin-top: 20px;
}

.sidebar-header {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>
