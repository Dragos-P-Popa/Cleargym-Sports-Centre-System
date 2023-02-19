const UserModel = require('../../users/models/users.model');
const crypto = require('crypto');

/*
    This file checks that user imputted email and passwords
    match what we have in the mongo database. 
*/

// module which checks if the given email and password
// matches what is in the db
exports.isMatch = (req, res, next) => {
    // find the user document of the given email
    UserModel.findByEmail(req.body.email).then((user) => {
        // if there is none, the email is not registered with
        if(!user[0]){
            res.status(404).send({});
        }else{
            // split encrypted password into hash and salt
            let passwordCombined = user[0].password.split('$');
            let salt = passwordCombined[0];
            // hash given password
            let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
            // if the hash of the given password is the same as the encrypted version in the db;
            if (hash === passwordCombined[1]) {
                req.body = {
                    userId: user[0]._id,
                    email: user[0].email,
                    permissionLevel: user[0].permissionLevel,
                    provider: 'email',
                    name: user[0].firstName + ' ' + user[0].lastName,
                };
                return next();
            } else {
                return res.status(400).send({errors: ['Invalid e-mail or password']});
            }
        }
    })
}