<template>
  <div id="app">
    <header class="header">
      <h1>タイトル</h1>
    </header>
    <main class="main-content">
      <Main />
    </main>
    <footer class="footer">
      フッター
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Main from './components/Main.vue';

export default defineComponent({
  name: 'App',
  components: {
    Main,
  },
});
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  background-color: #f5f5f5;
  padding: 16px;
  box-shadow: none;
  text-align: center;
}

.main-content {
  flex: 1;
  background-color: #f5f5f5;
  padding: 0 16px;
  display: flex;
  justify-content: center;
  height: calc(100% - 100px);
}

.footer {
  background-color: #f5f5f5;
  box-shadow: none;
  text-align: center;
}
</style>