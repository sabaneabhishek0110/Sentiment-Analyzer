const { PythonShell } = require( 'python-shell' )
const fs = require( 'fs' );
const path = require( 'path' );
const { spawn } = require( 'child_process' );

let emotions_count = {
    'anger': 0,
    'anticipation': 0,
    'disgust': 0,
    'fear': 0,
    'joy': 0,
    'sadness': 0,
    'surprise': 0,
    'trust': 0,
    'positive': 0,
    'negative': 0
}

const home = async ( req, res ) => {
    const reqData = req.body;
    // res.status(200).send("Home page of sentiment analysis");
    const filePath = path.join( __dirname, '../public/front_end/Sentiment_Analysis_FrontEnd.html' );
    console.log( req.url );
    return res.status( 200 ).sendFile( filePath );
}
/*
const analyzeContent = async ( req, res ) => {
    const { analysiscontent } = req.body;
    console.log( analysiscontent );
    // Save the content to a file that the Python script will read
    const filePath = "E:/abhishek/SA/Sentiment Analysis New 13-7-2024/Sentiment Analysis/Data/content.txt";
    try {
        await fs.promises.writeFile( filePath, analysiscontent );
    } catch ( error ) {
        console.error( 'Error writing file:', error );
        return res.status( 500 ).send( 'Error writing file' );
    }

    const options = {
        scriptPath: "E:/abhishek/SA/Sentiment Analysis New 13-7-2024/Sentiment Analysis",
        args: [filePath],
    }
    // const pyshell = new PythonShell('SentimentAnalysis.py', options);
    // Run the Python script
    PythonShell.run( 'SentimentAnalysis.py', options, ( err, result ) => {
        if ( err ) {
            console.error( 'Error running Python script:', err );
            return res.status( 500 ).send( 'Error running Python script' );
        }
        console.log(resu);
        // Parse the Python script output
        try {
            const output = JSON.parse( result[0] );
            console.log( 'Python script output:', output );
            console.log( result );
            for (let emotion in emotions_count) {
                if (output[emotion] !== undefined) {
                    emotions_count[emotion] = output[emotion];
                }
            }
            console.log(emotions_count);
            res.status(200).json({ emotions_count });
           // const final_path = path.join( __dirname, '../public/front_end/Sentiment_Analysis_FrontEnd.html' )
            //return res.status( 200 ).sendFile( final_path )
        } catch ( parseError ) {
            console.error( 'Error parsing Python script output:', parseError );
            res.status( 500 ).send( 'Error parsing Python script output' );
        }
    } );
};*/



const analyzeContent = async (req, res) => {
    const { analysiscontent } = req.body;
    console.log('Received content for analysis:', analysiscontent);
    const filePath = "D:/Sentiment Analysis/Data/content.txt";
    try {
        await fs.promises.writeFile( filePath, analysiscontent );
    } catch ( error ) {
        console.error( 'Error writing file:', error );
        return res.status( 500 ).send( 'Error writing file' );
    }
    const pythonProcess = spawn('python', ["D:/Sentiment Analysis/SentimentAnalysis.py", analysiscontent]);

    let outputData = '';
    pythonProcess.stdout.on('data', (data) => {
        outputData += data;

        const filePath = path.join( __dirname, '../public/front_end/Sentiment_Analysis_FrontEnd.html' );
       // return outputData;
        return res.status(200).json(outputData);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        res.status(500).json({ error: 'Error analyzing content' });
    });
};


// module.exports = { home,addContentInFile, analyzeContent ,...emotions_count};
module.exports = { home, analyzeContent };
// module.exports = output;