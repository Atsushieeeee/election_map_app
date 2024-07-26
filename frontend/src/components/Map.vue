<template>
  <div id="map"></div>
  <div ref="sidebar" class="sidebar">
    <div class="sidebar-header">{{ cityName }}</div>
    <button @click="closeSidebar" class="close-btn">×</button>
    <div class="chart-container">
      <canvas id="sidebarChart"></canvas>
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

export default defineComponent({
  name: 'Map',
  setup() {
    const selectedPolygon = ref<google.maps.Data.Feature | null>(null);
    const sidebar = ref<HTMLDivElement | null>(null);
    const chartData = ref<{ candidate_name: string; votes: number }[]>([]);
    const cityName = ref<string>('');
    let chartInstance: Chart | null = null; // チャートインスタンスを保持する変数

    const closeSidebar = () => {
      if (sidebar.value) {
        sidebar.value.classList.remove('visible');
        sidebar.value.classList.add('hidden');
      }
    };

    const showSidebar = () => {
      console.log('show?')
      if (sidebar.value) {
        sidebar.value.classList.remove('hidden');
        sidebar.value.classList.add('visible');
      }
    };

    const createChart = () => {
      const canvas = document.getElementById('sidebarChart') as HTMLCanvasElement;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          // 既存のチャートを破棄する
          if (chartInstance) {
            chartInstance.destroy();
          }

          chartInstance = new Chart(ctx, {
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
        } else {
          console.error('Canvas context not found');
        }
      } else {
        console.error('Canvas element not found');
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
          console.log(cityName.value)

          try {
            const votesResponse = await axios.get<Vote[]>('http://127.0.0.1:8000/api/votes/', {
              params: {
                city: name,
                election_date: '2024-07-07',
                region: '東京都'
              }
            });
            let votesData = votesResponse.data;

            // 得票数の多い順に並び替え
            votesData.sort((a, b) => b.votes - a.votes);

            // トップ10の候補者のみを表示
            chartData.value = votesData.slice(0, 10);

            showSidebar();  // サイドバーを表示

            // サイドバーが表示された後にチャートを描画
            nextTick(() => {
              createChart();
            });

          } catch (error) {
            console.error('得票データの読み込みに失敗しました', error);
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

    return { sidebar, chartData, closeSidebar, cityName };
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
