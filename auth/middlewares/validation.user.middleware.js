const jwt = require('jsonwebtoken');
const fs = require('fs');

/*
    This file checks that the given request contains
    a Bearer token. If this is present, it validates
    it using the public key.
*/

// open public key file
var publicKEY  = fs.readFileSync('public.key', 'utf8');

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