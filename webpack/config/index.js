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
      assetsSubDirectory: 'dist/webpack',
      assetsRoot: path.resolve(__dirname, './dist'),
    },
    dev: {
      assetsSubDirectory: 'dist/webpack',
      proxyTable: proxy,
    }
  }