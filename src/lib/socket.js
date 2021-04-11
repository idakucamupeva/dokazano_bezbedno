class Socket {

    constructor(server) {
        this.io = require('socket.io')(server);

        this.io.on('connection', socket => { 
            console.log("connected");                                  
            socket.on('disconnect', () => {
                console.log('diconnect');
            })   
            socket.on('getMails', (data) => {
                const program = "python3 /home/mihailo/Documents/FON_HAKTON/dokazano_bezbedno/src/API/test.py " + "Beograd " + "Krusevac " + "Kragujevac " + "Jagodina " + "Niš ";
                console.log(program)
                
                var child = require('child_process').exec(program)
                const exec = require("child_process").execSync;
                var result = exec(program);
                console.log(result.toString("utf8"));
                socket.emit("done", {nesto: result.toString("utf8")});
            })         
        });
    }
}

module.exports = Socket;
