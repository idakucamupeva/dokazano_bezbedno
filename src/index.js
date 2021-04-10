require('dotenv').config();

const classServer = require('./lib/server')
const Server = new classServer();
const server = Server.getServer();

const Socket = require('./lib/socket')
const socket = new Socket(server)