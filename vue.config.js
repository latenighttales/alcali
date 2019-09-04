module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    devServer: {
      proxy: {
        '/api*': {
          // Forward frontend dev server request for /api to django dev server
          target: 'http://localhost:8000/',
        }
      }
    }
  }
