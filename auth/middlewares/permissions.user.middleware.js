const UserModel = require('../../users/models/users.model');
const jwt = require('jsonwebtoken');
const fs = require('fs');
var publicKEY  = fs.readFileSync('public.key', 'utf8');

/*
    This file ensures that the user requesting a certain resource
    has the necessary permissions
*/

exports.minimumPermissionLevelRequired = (required_permission_level) => {
    return (req, res, next) => {
        const token = req.cookies.accessToken.slice(1, -1)

        if (token){
            // decode token
            decoded = jwt.decode(token, publicKEY);

            // find the user to which it belongs and return
            UserModel.findById(decoded.aud)
                .then((user) => {

                    if (user.privilegeLevel >= required_permission_level) {
                        next()
                    } else {
                        // user does not have necessary permissions
                        return res.status(401).send({error: "Unsufficient permissions"});
                    }
                });
        }
             
    };
 };