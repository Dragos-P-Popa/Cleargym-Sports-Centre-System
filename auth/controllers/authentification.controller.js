const jwt = require('jsonwebtoken');
const fs = require('fs');
const BlacklistModel = require('../models/tokens.model');
const UserModel = require('../../users/models/users.model');

/*
    This file creates the JWT tokens and adds refresh tokens
    to the blacklist once a user has been signed out
*/

// open the private key file
var privateKEY  = fs.readFileSync('private.key', 'utf8');

exports.login = (req, res) => {

    const user = UserModel.findByEmail(req.body.email).then((result) => {
        const uid = JSON.stringify(result[0]._id).slice(1, -1)

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

        // set the token settings
        var signOptionsRefresh = {
            issuer:  'Sports Centre System',
            expiresIn:  "2d",
            // the audience will be checked to make sure the 
            // correct user is making the request using a token which was 
            // assigned to them
            audience: uid,
            algorithm:  "RS256" 
            };

        // create tokens containing user ID and the signOptions
        // alongside expiry and issue time
        var accessToken = jwt.sign({user: uid}, privateKEY, signOptionsAccess);
        var refreshToken = jwt.sign({user: uid}, privateKEY, signOptionsRefresh);

        res.cookie("accessToken", JSON.stringify(accessToken), {
            secure: process.env.NODE_ENV !== "development",
            httpOnly: true
        });

        res.cookie("refreshToken", JSON.stringify(refreshToken), {
            secure: process.env.NODE_ENV !== "development",
            httpOnly: true
        });

        res.cookie("audience", uid, {
            secure: process.env.NODE_ENV !== "development",
            httpOnly: true
        });

        // send the tokens
        res.status(201).send({})
    });
    
}

exports.logout = (req, res) => {
    // if previous checks in routes.config pass and the token
    // has not been blacklisted already, it should be blacklisted now
    BlacklistModel.blacklistToken(req.body);
    return res.status(200).send({response: "Token has just been blacklisted"});
}