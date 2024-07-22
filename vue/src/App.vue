<template>
  <div id="app">
    <Map />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Map from './components/Map.vue';

export default defineComponent({
  name: 'App',
  components: {
    Map,
  },
});
</script>

<style>
/* 必要に応じてスタイルを追加 */
</style>
