const path = require('path');
const webpack = require('webpack');
module.exports = {
  mode: 'production',
  entry: './assets/build.js',
  output: {
    filename: 'testability.js',
    path: path.resolve(__dirname, 'src', 'SeleniumTestability', 'js')
  },
  plugins: [],
  module: {
    rules: [
      {
        test: require.resolve('testability-browser-bindings'),
        use: 'exports-loader?instrumentBrowser'
      }, {
        test: /.(js|jsx)$/,
        include: [path.resolve(__dirname, 'assets')],
        loader: 'babel-loader',

        options: {
          plugins: ['syntax-dynamic-import'],

          presets: [
            [
              '@babel/preset-env',
              {
                modules: false
              }
            ]
          ]
        }
      }
    ]
  },

  optimization: {
    minimize: true,
    splitChunks: {
      cacheGroups: {
        vendors: {
          priority: -10,
          test: /[\\/]node_modules[\\/]/
        }
      },

      chunks: 'async',
      minChunks: 1,
      minSize: 30000,
      name: true
    }
  },

  devServer: {
    open: true
  }
};
