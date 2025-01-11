const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

function x(t) {
    const l = new Uint16Array(t.length);
    console.log("L là gì: "+ l);
    
    for (let n = 0; n < l.length; n++)
        l[n] = t.charCodeAt(n);
    const o = new Uint8Array(l.buffer);
    let a = "";
    for (let n = 0; n < o.byteLength; n++)
        a += String.fromCharCode(o[n]);
    return btoa(le(le(a))) + "="
}

function le(t) {
    return btoa(t).split("").reverse().join("")
}

app.post('/api/process', (req, res) => {
    const inputData = req.body.data;
    if (!inputData) {
        return res.status(400).json({ error: 'No data provided' });
    }
    
    const result = x(inputData);
    res.json({ result: result });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
