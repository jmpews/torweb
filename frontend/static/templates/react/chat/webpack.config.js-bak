var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        app: './src/index.js',
        vendors: ['react', 'react-dom', 'react-redux']
    },
    output: {
        path: '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/assets/js/react',
        // path: path.join(__dirname, 'dist'),
        filename: '[name].min.js',
        publicPath: 'dist'
    },
    module: {
        loaders: [{
            test: /\.jsx?$/,
            loader: 'babel',
            exclude: /node_modules/,
            query: {
                presets: ["react", "es2015"]
            },
        }, {
            test: /\.css/,
            include: path.join(__dirname, 'dist'),
            loader: ExtractTextPlugin.extract("style-loader", "css-loader?modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]")
        }, {
            test: /\.(png|gif)$/,
            loader: "file-loader?name=img/[name]-[hash:8].[ext]"
        }]
    },
    resolve: {
      extensions: ['', '.js', '.jsx']
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                screw_ie8: true,
                warnings: false
            },
            sourceMap: false,
            minimize: true
        }),
        new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.min.js', Infinity),
        new ExtractTextPlugin("styles.css"),
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: JSON.stringify("production")
            }
        })
    ]
};

