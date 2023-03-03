const BlacklistModel = require('../models/tokens.model');

/*
    This file is used to control the functionality
    of the tokens model
*/

// check if a given refresh token has been blacklisted
exports.isBlacklisted = (req, res, next) => {
    const token = req.cookies.refreshToken.slice(1, -1)
    BlacklistModel.findByToken(token).then((result) => {
        if (result.length == 0){
            return next();
        } else {
            return res.status(200).send({response: "Token is blacklisted"});
        }
    });
}