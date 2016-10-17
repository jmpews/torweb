//webpack.config.js

var webpack = require('webpack');

module.exports = {
  entry: [
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
  plugins: [
    new webpack.DefinePlugin({
        'process.env': {
              'NODE_ENV': JSON.stringify('production')
            }
      }),
  ]
};
