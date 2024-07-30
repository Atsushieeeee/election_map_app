<template>
  <div id="map" class="map-container"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'Map',
  emits: ['polygon-click'],
  setup(_, { emit }) {
    const selectedPolygon = ref<google.maps.Data.Feature | null>(null);
    const map = ref<google.maps.Map | null>(null);

    onMounted(async () => {
      const mapOptions: google.maps.MapOptions = {
        center: { lat: 35.682839, lng: 139.759455 },
        zoom: 10,
      };

      map.value = new google.maps.Map(document.getElementById('map') as HTMLElement, mapOptions);

      try {
        const response = await axios.get('/tokyo.geojson');
        const geoJsonData = response.data;

        map.value.data.addGeoJson(geoJsonData);

        map.value.data.setStyle((feature) => {
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

        map.value.data.addListener('click', (event: google.maps.Data.MouseEvent) => {
          if (selectedPolygon.value) {
            map.value.data.revertStyle(selectedPolygon.value);
          }

          selectedPolygon.value = event.feature;

          map.value.data.overrideStyle(selectedPolygon.value, {
            fillColor: '#0000FF',
            fillOpacity: 0.5,
            strokeColor: '#4052a2',
            strokeOpacity: 0.8,
            strokeWeight: 2,
          });

          const feature = event.feature;
          const name = feature.getProperty('N03_004') as string;
          emit('polygon-click', name);
        });
      } catch (error) {
        console.error('ポリゴンデータの読み込みに失敗しました', error);
      }
    });

    return {};
  },
});
</script>

<style scoped>
#map {
  width: 100%;
  height: 100%;
}
</style>
