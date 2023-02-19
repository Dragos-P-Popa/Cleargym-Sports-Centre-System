const jwt = require('jsonwebtoken');
const fs = require('fs');

/*
    This file creates the JWT token
*/

// open the private key file
var privateKEY  = fs.readFileSync('private.key', 'utf8');

exports.login = (req, res) => {

    // set the token settings
    var signOptions = {
    issuer:  'Sports Centre System',
    expiresIn:  "12h",
    // the audience will be checked to make sure the 
    // correct user is making the request using a token which was 
    // assigned to them
    audience: req.body.email,
    algorithm:  "RS256" 
    };

    // create token containing user ID and the signOptions
    // alongside expiry and issue time
    var token = jwt.sign({user: req.body.id}, privateKEY, signOptions);

    // send the token
    res.status(201).send({accessToken: token})
}