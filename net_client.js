const net = require('net');

const client = net.createConnection({
	host:'127.0.0.1',
	port:9191,
});

var test = '';

client.on('data', (data) => {

	test += data;
	console.log('asdf  : ' + test.toString());
})