<template>
  <div class="sidebar">
    <div class="sidebar-wrap">
      <div class="text-subtitle-1">選挙得票数可視化サイト</div>

      <v-expansion-panels v-model="panel" multiple>
        <v-expansion-panel>
          <v-expansion-panel-title>
            <label class="text-subtitle-2" for="">選挙選択</label>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-select
              density="comfortable"
              label="選挙"
              :items="['東京都知事選']"
              variant="outlined"
            ></v-select>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-title>
            <label class="text-subtitle-2" for="">エリアを選択</label>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-select
              density="comfortable"
              label="市区町村"
              :items="['千代田区', '港区']"
              variant="outlined"
            ></v-select>
          </v-expansion-panel-text>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-title>
            <label class="text-subtitle-2" for="">ヒートマップ</label>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-radio-group>
              <v-radio label="得票数" value="one" color="primary"></v-radio>
              <v-radio label="人口" value="two" color="primary"></v-radio>
              <v-radio label="収入" value="three" color="primary"></v-radio>
            </v-radio-group>
          </v-expansion-panel-text>
        </v-expansion-panel>

      </v-expansion-panels>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      panel: [0, 1, 2]
    }
  }
};
</script>

<style scoped>
.sidebar {
  padding: 16px 0 16px 16px;
}
.sidebar-wrap {
  height: 100%;
  width: 100%;
  background: #fff;
  border-radius: 4px;
}

.text-subtitle-1 {
  padding: 16px 12px;
}

.sidebar-select {
  padding: 16px 8px 0 8px;
}
</style>
