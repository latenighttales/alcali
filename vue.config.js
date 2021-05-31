module.exports = {
  chainWebpack: (config) => {
    config.module
      .rule("i18n")
      .resourceQuery(/blockType=i18n/)
      .type("javascript/auto")
      .use("i18n")
      .loader("@kazupon/vue-i18n-loader")
      .end();
  },
  outputDir: "dist",
  assetsDir: "static",
  devServer: {
    proxy: {
      "/api*": {
        // Forward frontend dev server request for /api to django dev server
        target: "http://localhost:8000/",
      },
    },
  },
};
