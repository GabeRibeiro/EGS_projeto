const express = require('express')
const dotenv = require('dotenv')
const app = express()
const mongoose = require('mongoose')
const bcrypt = require('bcryptjs')
const User = require('./model/User')
const jwt = require('jsonwebtoken')
const verify = require('./routes/verifyToken')
const { registerValidation, loginValidation } = require('./validation')

const url = 'mongodb://root:123456@mongo:27017';

app.set('view-engine', 'ejs')



dotenv.config();


mongoose.Promise = global.Promise
//Connect to DB
mongoose.connect(
        url , {
        useNewUrlParser: true, 
        useUnifiedTopology: true
    }, (err, client) => {
        if (err) {
            return console.log(err);
        }
    
        console.log('connected to mongodb:' + url);
    }); 

//Middleware
app.use(express.json())
app.use(express.urlencoded({ extended: false }))


app.get('/register', (req, res) => {
    res.render('register.ejs')
})

app.get('/login', (req, res) => {
    res.render('login.ejs')
})

app.post('/register', async (req, res) => {
    //Validate
    const { error } = registerValidation(req.body)
    if(error) return res.status(400).send(error.details[0].message) 

    //Check if user already exists
    const emailExists = await User.findOne({email: req.body.email})
    if(emailExists) return res.status(400).send('Email already exists')


    //Hash passwords
    const salt = await bcrypt.genSalt(10)
    const hashedPassword = await bcrypt.hash(req.body.password, salt)

    //Create user
    const user = new User({
        name: req.body.name,
        email: req.body.email,
        password: hashedPassword
    })

    try {
        const savedUser = await user.save()
        res.send({user: user._id})
    } catch (err) {
        res.status(400).send(err)
    }
})

//LOGIN
app.post('/login', async (req, res) => {
    //Validate
    const { error } = loginValidation(req.body)
    if(error) return res.status(400).send(error.details[0].message) 

    //Check if user exists
    const user = await User.findOne({email: req.body.email})
    if(!user) return res.status(400).send('Email wrong')

    //Check if password is correct
    const validPW = await bcrypt.compare(req.body.password, user.password)
    if(!validPW) return res.status(400).send('Password wrong')
    
    //Create and assign a token
    const token = jwt.sign({_id: user._id}, process.env.TOKEN_SECRET, {expiresIn: '6h'})
    res.header('auth-token', token).send({user: user._id}).status(200)
    
})



app.post('/verifyToken', verify,  async (req,res) => {

    res.json({
        message: 'Sucessfully logged in',
    })
    res.status(200)
    
    
})



app.listen(3000, () => console.log('Server running'))

