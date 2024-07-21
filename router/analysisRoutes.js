const express = require('express')
const router = express.Router()
const { analyzeContent, home } = require('../controller/analysisController')

router.get("/home", home);
// router.post("/addContent",addContentInFile);
router.post("/analyze", analyzeContent);

module.exports = router;