const express = require('express')
const router = express.Router()

const {addContentInFile,home} = require('../controller/analysis_controller')

router.get('/home',home)
router.post('/analyze',addContentInFile)

module.exports = router