module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/smart-meeting-system/'
    : '/',

  devServer: {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': 'true',
      'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS,POST,PUT',
      'Access-Control-Allow-Headers':
      'Origin, X-Requested-With, Content-Type, Accept, Authorization',
      "Referrer-Policy":  "no-referrer-when-downgrade",
      "Cross-Origin-Opener-Policy": "same-origin, same-origin-allow-popups" 
    },
    proxy: 'http://localhost:8080',
  }

//   headers: { "Referrer-Policy": "no-referrer-when-downgrade",
// "Cross-Origin-Opener-Policy": "same-origin-allow-popups" }

  // proxyTable: {
  //   '/scheduling': {
  //     target:'http://localhost:8080/',
  //     changeOrigin:true,
  //     pathRewrite:{
  //       '^/scheduling': ''
  //     }
  //   }
  // }
}