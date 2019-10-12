const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './src/app.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'app.bundle.js',
  },
  plugins: [
    new HtmlWebpackPlugin({
      inject: true,
      hash: true,
      title: 'Twitter AI Application',
      template: './src/index.html',
      filename: './index.html',
    }),
  ],
};
