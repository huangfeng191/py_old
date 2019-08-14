var path=require("path")
var proxy = {};
// var mods = ["**/*.json","/stock/interfaceconfig.html"];
var mods = ["**/*.json","**/ctx.js", "/ctx.js",
"/static/Scripts/****",
"/static/stock/****",
"/static/prostock/****",
"/static/Skins/****",
"/static/Scripts/MyDialog/****",
"/stock/**.html",
"/prostock/**.html",
"/static/graphic/****",
"/upload",
"/static/gis/****",
"/static/spread/****",
"/static/Scripts/CRUD/****",
"/static/baoxing/js/localBand.js",
"/static/Scripts/CRUD/**",
"/stock/bindings.js",
"/prostock/bindings.js",
"/biz/*",
"/static/md/***",
"/v.png","/upload","/export","/logout.html"];

var server="http://localhost:82";
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