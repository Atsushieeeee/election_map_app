import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // Vuetifyの設定ファイル

createApp(App)
  .use(vuetify)
  .mount('#app');
