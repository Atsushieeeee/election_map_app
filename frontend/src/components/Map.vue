<template>
  <div id="map" class="map-container"></div>
  <Sidebar
    :cityName="cityName"
    :show="sidebarVisible"
    @update:show="sidebarVisible = $event"
  />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import axios from 'axios';
import Sidebar from './Sidebar.vue';

export default defineComponent({
  name: 'Map',
  components: {
    Sidebar,
  },
  setup() {
    const selectedPolygon = ref<google.maps.Data.Feature | null>(null);
    const cityName = ref<string>('');
    const sidebarVisible = ref<boolean>(false);

    const closeSidebar = () => {
      sidebarVisible.value = false;
    };

    const showSidebar = () => {
      sidebarVisible.value = true;
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
          showSidebar()

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

    return { cityName, sidebarVisible, closeSidebar };
  },
});
</script>

<style scoped>
#map {
  position: absolute;
  width: 100%;
  height: calc(100% - 95px);
}
</style>
