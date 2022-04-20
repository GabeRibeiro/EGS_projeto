const express = require('express')
const dotenv = require('dotenv')
const app = express()
const mongoose = require('mongoose')

//Import routes
const authRoute = require('./routes/auth')

dotenv.config();

//Connect to DB
mongoose.connect(
    process.env.DB_CONNECT 
    ,{useNewUrlParser: true}
    ,() => console.log('connected to mongodb'))


//Middleware
app.use(express.json())

//Route middlewares
app.use('/api/user',authRoute)

app.listen(3000, () => console.log('Server running'))

