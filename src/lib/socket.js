class Socket {

    constructor(server) {
        this.io = require('socket.io')(server);

        this.io.on('connection', socket => {                                   
            socket.on('disconnect', () => {
                console.log('diconnect');
            })            
        });
    }
}

module.exports = Socket;
