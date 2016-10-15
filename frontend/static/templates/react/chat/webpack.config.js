//webpack.config.js

var webpack = require('webpack');

module.exports = {
  entry: [
  	'webpack-dev-server/client?http://0.0.0.0:3000', // WebpackDevServer host and port
    'webpack/hot/only-dev-server',
    './src/index.js'
  ],
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
     loaders: ['babel']
    }],
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  output: {
	path: '/Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/assets/js/react',
	//path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: './dist',
    hot: true
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ]
};
