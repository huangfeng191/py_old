var path = require('path')
var webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')

var config = require('./config')


//path:编译路径地址， 原来 ./dist
module.exports = {
    entry: {
        app:path.join(__dirname,'src','main.js'),
        out:path.join(__dirname,'src',"framework",'main.js'),
    },
    output: {
        // path: path.resolve(__dirname, './dist'),
        path: path.resolve(__dirname, '../src/templates/webpack'),
    //  导入的资源 
        // publicPath: '/dist/',
        // publicPath : 'www.baidu.com'//若有地址，则打包会变为上线地址
        // filename: 'build.js'
        // filename: '[name]-[chunkhash].js'
        // filename: '../../static/webpack/[name].js'
        filename: '[name].js'

    },
    externals: {

    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {}
                    // other vue-loader options go here
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
                loader: 'file-loader'
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.less$/,
                loader: "style-loader!css-loader!less-loader",
            },
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    /**
     devServer: {
    historyApiFallback: true,
    hot: true,
    inline: true,
    progress: true,
    port: 3000,
    host: '10.0.0.9',
    proxy: {
      '/test/*': {
        target: 'http://localhost',
        changeOrigin: true,
        secure: false
      }
    }
  },
     */

    devServer: {
        // contentBase: path.join(__dirname, "dist"),
        // 它指定了服务器资源的根目录，如果不写入contentBase的值，那么contentBase默认是项目的目录。
        historyApiFallback: true,
        noInfo: true,
        proxy: config.dev.proxyTable
    },
    performance: {
        hints: false
    },
    devtool: '#eval-source-map'
}
if(process.env.NODE_ENV==="development"){
    module.exports.plugins=(module.exports.plugins||[]).concat([
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: true,
            // 关联 entry 里面的 key
            // 就是绑定的js 生成
            // inject是生成html文件的时候要不要把模板中的的html引入的js也一起带进去;默认是true的;
            chunks:['app']
          }),
        new HtmlWebpackPlugin({
            filename: 'out.html',
            template: 'out.html',
            inject: true,
            // 关联 entry 里面的 key
            // 就是绑定的js 生成
            chunks:['out']
          }),
    ])
}
if (process.env.NODE_ENV === 'production') {

    module.exports.devtool = '#source-map'
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            //sourceMap: true,  build 是否输出map内容
            sourceMap: false,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        }),

        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
          }),
        // The plugin will generate an HTML5 file for you that includes 
        // all your webpack bundles in the body using script tags.
        //  Just add the plugin to your webpack config as follows:
/*         new HtmlWebpackPlugin({
            filename:'../index.html',
            // 已某个文件作为模板,在把生成的添加进去
            template:'./indexpro.html'
        }) */
        //  此设置 是将index.html 移动到目标 output.path 

        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: true,
            hash:true,
            // 关联 entry 里面的 key
            // 就是绑定的js 生成
            // inject是生成html文件的时候要不要把模板中的的html引入的js也一起带进去;默认是true的;
            chunks:['app']
          }),
        new HtmlWebpackPlugin({
            filename: 'out.html',
            template: 'out.html',
            inject: true,
            // 关联 entry 里面的 key
            // 就是绑定的js 生成
            chunks:['out']
          }),


    ])
}

