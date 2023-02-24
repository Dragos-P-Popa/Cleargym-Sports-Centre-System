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
    // if the header contains a token
    if(req.headers['authorization']) {
        try {
            let auth = req.headers['authorization'].split(' ');
            // check that the authorisation header type is 'Bearer'
            if (auth['0'] !== 'Bearer') {
                // if not, unauthorised
                return res.status(401).send();
            } else {
                // if the key is valid, next() is called and the logic continues 
                // in another controller based on route
                req.jwt = jwt.verify(auth[1], publicKEY);
                return next();
            }
        } catch (e) {
            return res.status(403).send();
        }
    } else {
        // return unauthorised as there is no token present
        return res.status(401).send();
    }
};

exports.checkRefresh = (req, res) => {
    if (req.body.refreshToken){
        decoded = jwt.decode(req.body.refreshToken, publicKEY)

        if ((decoded.aud == req.body.audience) && jwt.verify(req.body.refreshToken, publicKEY)) {
            // set the token settings
            var signOptionsAccess = {
                issuer:  'Sports Centre System',
                expiresIn:  "10m",
                // the audience will be checked to make sure the 
                // correct user is making the request using a token which was 
                // assigned to them
                audience: req.body.audience,
                algorithm:  "RS256" 
                };

            var accessToken = jwt.sign({user: req.body.audience}, privateKEY, signOptionsAccess);

            res.status(201).send({accessToken: accessToken})
        } else {
            return res.status(401).send({error: "Wrong audience"});
        }
    } else {
        return res.status(400).send({error: "Refresh token is missing."});
    }
}