import express from 'express';
import fs from 'fs';

const router = express.Router();
const logfile = fs.readFileSync("./routes/logs.json");
var jsondata = JSON.parse(logfile);

router.post('/:submit', (req,res) => {
    console.log(req.body);
    jsondata.push(req.body);
    res.send("Data submitted");

});


router.get('/:data', (req,res) => {
    res.send(jsondata);
    // console.log(jsondata);
})





export default router