<template>
  <div id="map"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'Map',
  setup() {
    const selectedPolygon = ref<google.maps.Data.Feature | null>(null);

    onMounted(async () => {
      const mapOptions: google.maps.MapOptions = {
        center: { lat: 35.682839, lng: 139.759455 }, // 東京都の中心座標
        zoom: 10,
      };

      const map = new google.maps.Map(document.getElementById('map') as HTMLElement, mapOptions);

      try {
        // ポリゴンデータの取得
        const response = await axios.get('/tokyo.geojson');
        const geoJsonData = response.data;

        // ポリゴンの描画
        map.data.addGeoJson(geoJsonData);

        // ポリゴンのスタイル設定
        map.data.setStyle((feature) => {
          const defaultStyle = {
            fillColor: '#D3D3D3', // 薄いグレーカラー
            fillOpacity: 0.5,     // ポリゴンの不透明度
            strokeColor: '#4052a2', // 濃いグレーカラー
            strokeOpacity: 0.8,
            strokeWeight: 2,
          };

          if (feature === selectedPolygon.value) {
            return {
              fillColor: '#0000FF', // 濃い青
              fillOpacity: 0.5,
              strokeColor: '#4052a2',
              strokeOpacity: 0.8,
              strokeWeight: 2,
            };
          }

          return defaultStyle;
        });

        // ポリゴンをクリックしたときのイベントリスナーを追加
        map.data.addListener('click', (event: google.maps.Data.MouseEvent) => {
          if (selectedPolygon.value) {
            // 前回選択されたポリゴンの色を元に戻す
            map.data.overrideStyle(selectedPolygon.value, {
              fillColor: '#D3D3D3',
              fillOpacity: 0.5,
              strokeColor: '#4052a2',
              strokeOpacity: 0.8,
              strokeWeight: 1.5,
            });
          }

          // 新しく選択されたポリゴンの色を変更する
          selectedPolygon.value = event.feature;
          const feature = event.feature;
          const name = feature.getProperty('N03_004');
          console.log(name)
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

    return {};
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
