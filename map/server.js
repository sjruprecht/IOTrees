/*
  Can't remember why we needed this express server...
  Can probably delete this.
*/

var express = require('express')
var app = express()

app.use(express.static('public'))
// respond with "hello world" when a GET request is made to the homepage
app.get('/', function (req, res) {

});

app.listen(3000)
