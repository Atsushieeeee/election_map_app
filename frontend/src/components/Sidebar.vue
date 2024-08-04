<template>
  <div class="sidebar">
    <div class="text-subtitle-1">選挙得票数可視化サイト</div>
    <label class="text-subtitle-2" for="">選挙選択</label>
    <v-select
      label="選挙"
      :items="['東京都知事選']"
      variant="outlined"
    ></v-select>
    <label class="text-subtitle-2" for="">エリアを選択</label>
    <v-select
      label="市区町村"
      :items="['千代田区', '港区']"
      variant="outlined"
    ></v-select>

    <v-radio-group>
      <v-radio label="得票数" value="one" color="primary"></v-radio>
      <v-radio label="人口" value="two" color="primary"></v-radio>
      <v-radio label="収入" value="three" color="primary"></v-radio>
    </v-radio-group>

  </div>
</template>

<script>
export default {
  name: 'Sidebar',
};
</script>

<style scoped>
.sidebar {
  padding: 10px;
}
</style>
