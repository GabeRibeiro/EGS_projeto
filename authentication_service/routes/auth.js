const router = require('express').Router()
const bcrypt = require('bcryptjs')
const User = require('../model/User')
const jwt = require('jsonwebtoken')
const { registerValidation, loginValidation } = require('../validation')



router.post('/register', async (req, res) => {
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
router.post('/login', async (req, res) => {
    //Validate
    const { error } = loginValidation(req.body)
    if(error) return res.status(400).send(error.details[0].message) 

    //Check if user already exists
    const user = await User.findOne({email: req.body.email})
    if(!user) return res.status(400).send('Email wrong')

    //Check if password is correct
    const validPW = await bcrypt.compare(req.body.password, user.password)
    if(!validPW) return res.status(400).send('Password wrong')
    
    //Create and assign a token
    const token = jwt.sign({_id: user._id}, process.env.TOKEN_SECRET)
    res.header('auth-token', token).send(token)

})





module.exports = router