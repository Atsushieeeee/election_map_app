<template>
  <div id="map"></div>
  <div ref="sidebar" class="sidebar">
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
import { defineComponent, onMounted, ref, nextTick } from 'vue';
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
  name: 'Map',
  setup() {
    const selectedPolygon = ref<google.maps.Data.Feature | null>(null);
    const sidebar = ref<HTMLDivElement | null>(null);
    const chartData = ref<Vote[]>([]);
    const ageGroupData = ref<AgeGroup[]>([]);
    const cityName = ref<string>('');
    const totalPopulation = ref<number | null>(null);
    let chartInstance: Chart | null = null; // 得票数のチャートインスタンス
    let populationChartInstance: Chart | null = null; // 人口分布のチャートインスタンス

    const closeSidebar = () => {
      if (sidebar.value) {
        sidebar.value.classList.remove('visible');
        sidebar.value.classList.add('hidden');
      }
    };

    const showSidebar = () => {
      if (sidebar.value) {
        sidebar.value.classList.remove('hidden');
        sidebar.value.classList.add('visible');
      }
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

    onMounted(async () => {
      const mapOptions: google.maps.MapOptions = {
        center: { lat: 35.682839, lng: 139.759455 },
        zoom: 10,
      };

      const map = new google.maps.Map(document.getElementById('map') as HTMLElement, mapOptions);

      try {
        const response = await axios.get('/tokyo.geojson');
        const geoJsonData = response.data;

        map.data.addGeoJson(geoJsonData);

        map.data.setStyle((feature) => {
          const defaultStyle = {
            fillColor: '#D3D3D3',
            fillOpacity: 0.5,
            strokeColor: '#4052a2',
            strokeOpacity: 0.8,
            strokeWeight: 2,
          };

          if (feature === selectedPolygon.value) {
            return {
              fillColor: '#0000FF',
              fillOpacity: 0.5,
              strokeColor: '#4052a2',
              strokeOpacity: 0.8,
              strokeWeight: 2,
            };
          }

          return defaultStyle;
        });

        map.data.addListener('click', async (event: google.maps.Data.MouseEvent) => {
          if (selectedPolygon.value) {
            map.data.overrideStyle(selectedPolygon.value, {
              fillColor: '#D3D3D3',
              fillOpacity: 0.5,
              strokeColor: '#4052a2',
              strokeOpacity: 0.8,
              strokeWeight: 1.5,
            });
          }

          selectedPolygon.value = event.feature;
          const feature = event.feature;
          const name = feature.getProperty('N03_004') as string;
          cityName.value = name;

          try {
            const votesResponse = await axios.get<Vote[]>('http://127.0.0.1:8000/api/votes/', {
              params: {
                city: name,
                election_date: '2024-07-07',
                region: '東京都'
              }
            });
            chartData.value = votesResponse.data.sort((a, b) => b.votes - a.votes).slice(0, 10);

            const populationResponse = await axios.get('http://127.0.0.1:8000/api/population_distribution/', {
              params: {
                region: name
              }
            });
            const populationData = populationResponse.data;
            ageGroupData.value = populationData.age_groups;
            totalPopulation.value = populationData.total_population;

            showSidebar();

            nextTick(() => {
              createCharts();
            });

          } catch (error) {
            console.error('データの読み込みに失敗しました', error);
          }

          map.data.overrideStyle(selectedPolygon.value, {
            fillColor: '#0000FF',
            fillOpacity: 0.5,
            strokeColor: '#4052a2',
            strokeOpacity: 0.8,
            strokeWeight: 1.5,
          });
        });
      } catch (error) {
        console.error('ポリゴンデータの読み込みに失敗しました', error);
      }
    });

    return { sidebar, chartData, closeSidebar, cityName, totalPopulation };
  },
});
</script>

<style scoped>
html, body, #app, #map {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#map {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

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
