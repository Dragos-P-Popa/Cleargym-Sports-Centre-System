const jwt = require('jsonwebtoken');
const fs = require('fs');

/*
    This file creates the JWT tokens
*/

// open the private key file
var privateKEY  = fs.readFileSync('private.key', 'utf8');

exports.login = (req, res) => {

    // set the token settings
    var signOptionsAccess = {
        issuer:  'Sports Centre System',
        expiresIn:  "10m",
        // the audience will be checked to make sure the 
        // correct user is making the request using a token which was 
        // assigned to them
        audience: req.body.email,
        algorithm:  "RS256" 
        };

    // set the token settings
    var signOptionsRefresh = {
        issuer:  'Sports Centre System',
        expiresIn:  "2d",
        // the audience will be checked to make sure the 
        // correct user is making the request using a token which was 
        // assigned to them
        audience: req.body.email,
        algorithm:  "RS256" 
        };

    // create tokens containing user ID and the signOptions
    // alongside expiry and issue time
    var accessToken = jwt.sign({user: req.body.email}, privateKEY, signOptionsAccess);
    var refreshToken = jwt.sign({user: req.body.email}, privateKEY, signOptionsRefresh);

    // send the tokens
    res.status(201).send({accessToken: accessToken, refreshToken: refreshToken})
}