const jwt = require('jsonwebtoken')


module.exports = function (req, res, next){
    const token = req.header('auth-token')
    token = token
    if (!token) return res.status(401).send('Access Denied')

    try {
        const verified = jwt.verify(token, process.env.TOKEN_SECRET)
        req.user = verified
        res.status(200).send("Token verified successfully!")
    } catch (error) {
        res.status(400).send("Token failed to verify!")
    }
}