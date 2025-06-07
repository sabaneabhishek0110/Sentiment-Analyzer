const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const app = express();

const analysisRoutes = require('./router/analysisRoutes');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("./public"));
// app.use(express.static(path.join(__dirname,'front_end')));
app.use('/sentiment',analysisRoutes);

app.listen(5000,()=>{
    console.log('Litening port no 5000...');
})