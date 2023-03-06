const jwt = require('jsonwebtoken');
const fs = require('fs');
const BlacklistModel = require('../models/tokens.model');

/*
    This file checks that the given request contains
    a Bearer token. If this is present, it validates
    it using the public key.
*/

// open public key file
var publicKEY  = fs.readFileSync('public.key', 'utf8');
var privateKEY  = fs.readFileSync('private.key', 'utf8');

exports.checkJWT = (req, res, next) => {

    const token = req.cookies.accessToken.slice(1, -1)

    // if the header contains a token
    if(token) {
        try {
            // if the key is valid, next() is called and the logic continues 
            // in another controller based on route
            req.jwt = jwt.verify(token, publicKEY);
            return next();

        } catch (e) {
            console.log(e)
            return res.status(403).send({});
        }
    } else {
        // return unauthorised as there is no token present
        return res.status(401).send();
    }
};

exports.checkRefresh = (req, res) => {

    const token = req.cookies.refreshToken.slice(1, -1)
    const uid = req.cookies.audience

    if (token){
        decoded = jwt.decode(token, publicKEY)

        if ((decoded.aud == uid) && jwt.verify(token, publicKEY)) {
            // set the token settings
            var signOptionsAccess = {
                issuer:  'Sports Centre System',
                expiresIn:  "10m",
                // the audience will be checked to make sure the 
                // correct user is making the request using a token which was 
                // assigned to them
                audience: uid,
                algorithm:  "RS256" 
                };

            var accessToken = jwt.sign({user: uid}, privateKEY, signOptionsAccess);

            res.cookie("accessToken", JSON.stringify(accessToken), {
                secure: true,
                httpOnly: true
              });
            
            res.status(201).send({})
        } else {
            return res.status(401).send({error: "Wrong audience"});
        }
    } else {
        return res.status(400).send({error: "Refresh token is missing."});
    }
}