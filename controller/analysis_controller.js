const fs = require('fs')
const path = require('path')
const { spawn } = require('child_process');

const home = async (req,res)=>{
    const readData = req.body
    const filepath = path.join(__dirname,'../public/front_end/Sentiment_Analysis_FrontEnd.html');
    res.status(200).sendFile(filepath);
}

// const  addContentInFile = async (analysiscontent)=>{
//     try {
//         fs.writeFile('../Sentiment Analysis/Data/read.txt',analysiscontent,(err)=>{
//             if(err){
//                 console.log('error in writing the file')
//                 return res.status(500).send('internal server error ')
//             }
//         })
//         res.status(200).send('sucessfully sended')
//     } catch (error) {
//         console.log(error.message,"....")
//     }
// }

const addContentInFile = async (analysiscontent)=>{
    try {
       // const filePath = path.join(__dirname, '../content.txt');
        fs.writeFile('../Sentiment Analysis/Data/content.txt', analysiscontent, (err) => 
        {
            if(err){
                console.log('error in writing the file');
                console.log('\n\n', err.message);
                return res.status(500).send('internal server error ')
            }

            // res.status(200).send('Content fetched successfully!!');
        });

        
    } catch (error) {
        console.log(error.message)
    }
}
const analyzeContent = async (req, res) => {
    const { analysiscontent } = req.body
    console.log({analysiscontent});

    if(!analysiscontent){
        return res.status(400).send('please enter the data for analysis');
    }

    await addContentInFile(analysiscontent);
    // try {
    //     const output = await runPythonModel(2);
    //     console.log(output);
    //     const result = JSON.parse(output);
    //     res.status(200).json(result);
    // } catch (error) {
    //     console.error("Error running model:", error);
    //     res.status(500).send('Error running model');
    // }

};

// function runPythonModel(n) {
//     return new Promise((resolve, reject) => {
//         const pythonProcess = spawn('python3', ['SentimentAnalysis.py', n]);

//         let output = '';

//         pythonProcess.stdout.on('data', (data) => {
//             output += data.toString();
//         });

//         pythonProcess.stderr.on('data', (data) => {
//             reject(data.toString());
//         });

//         pythonProcess.on('close', (code) => {
//             if (code === 0) {
//                 resolve(output);
//             } else {
//                 reject(`Python script exited with code ${code}`);
//             }
//         });
//     });
// }

module.exports = {addContentInFile,home};