const express = require('express');
const app = express();


app.use(express.urlencoded({extended : false}));
app.use(express.json());

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');

    next();
});

app.use(express.static(process.env.PATH_WEB));

app.get('/', (req, res) => {
    res.sendFile(process.env.PATH_HTML);
});


module.exports = app;