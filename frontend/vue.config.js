module.exports = {
  devServer: {
    port: 8081, // 使用するポート番号を指定
    host: 'localhost',
    https: false,
    hot: true,
    proxy: 'http://127.0.0.1:8000',
  },
};
