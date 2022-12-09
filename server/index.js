import express from 'express';
import bodyParser from 'body-parser';
import router from './routes/routes.js';

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.use(function(req,res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Credentials', true);
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

app.listen(port, () => console.log(`Server is running on http://localhost:${port}/`));

app.use('/',router);