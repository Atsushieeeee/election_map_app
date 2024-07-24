<template>
  <div id="map"></div>
  <v-dialog v-model="dialog" max-width="800">
    <v-card>
      <v-card-title>得票数</v-card-title>
      <v-card-text>
        <canvas id="votesChart"></canvas>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="dialog = false">閉じる</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
    const dialog = ref(false);

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
          const name = feature.getProperty('N03_004');
          console.log(name)

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
            const topNVotesData = votesData.slice(0, 10);

            const candidateNames = topNVotesData.map((vote) => vote.candidate_name);
            const votes = topNVotesData.map((vote) => vote.votes);

            dialog.value = true;  // ダイアログを表示
            console.log(dialog.value)
             // ダイアログが表示されるタイミングでチャートを描画
            nextTick(() => {
              const ctx = (document.getElementById('votesChart') as HTMLCanvasElement).getContext('2d');
              if (ctx) {
                new Chart(ctx, {
                  type: 'bar',
                  data: {
                    labels: candidateNames,
                    datasets: [{
                      label: '得票数',
                      data: votes,
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

    return { dialog };
  },
});
</script>

<style>
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
</style>
