

var net = require('net');
var exec = require('child_process').exec;


var server = net.createServer(function(socket) {
	socket.write('Echo server\r\n');
  socket.on('data', function (data) {
  	console.log(data.toString('utf8'));
		exec('python3 map.py --data ' + data.toString('utf8') )
 	});
	socket.pipe(socket);
});

server.listen(3010, '0.0.0.0');
