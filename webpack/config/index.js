var path=require("path")
var proxy = {};
var mods = ["**/*.json","/stock/interfaceconfig.html"];
var server="http://localhost:8087";
for (let i = 0; i < mods.length; i++) {
  const mod = mods[i];
  proxy[mod] = {
    target: server,
    changeOrigin: true,//是否跨域
    secure: false
  };
}
module.exports = {
    build: {
      // index: path.resolve(__dirname, '../dist/templates/index.html'),
      // out: path.resolve(__dirname, '../dist/templates/out.html'),

      index: path.resolve(__dirname, '../../src/templates/webpack/index.html'),
      out: path.resolve(__dirname, '../../src/templates/webpack/out.html'),
      
      assetsSubDirectory: 'static/webpack',
      // assetsSubDirectory: 'webpack',
      // assetsRoot: path.resolve(__dirname, '../dist'),
      assetsRoot: path.resolve(__dirname, '../../src'),
      assetsPublicPath: '/',
      
    },
    dev: {
      assetsSubDirectory: 'webpack',
      proxyTable: proxy,
      assetsPublicPath: '/',
    }
  }