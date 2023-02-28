const UserModel = require('../../users/models/users.model');
const crypto = require('crypto');

/*
    This file checks that user imputted email and passwords
    match what we have in the mongo database. 
*/

exports.checkPassword = (req, res, next) => {
    // regex expression for strings that contain at least 6 chars, upper/lower case, number and symbol
    var re = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{6,}$/;

    // check if given password contains all of the criteria mentioned above
    if (re.test(req.body.password)){
        return next();
    } else {
        return res.status(400).send({error: "The password is not secure enough."});
    }
}

// module which checks if the given email and password
// matches what is in the db
exports.isMatch = (req, res, next) => {
    // check that the request contains all necessary fields
    if (req.body.email && req.body.password){
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
    } else {
        return res.status(400).send({error: "The request is missing fields."});
    }
}

// tests of POST request on the /users endpoint
exports.verifyUserCreation = (req, res, next) => {
    // check that the request body contains all required fields
    if (req.body.password && req.body.email && req.body.firstName && req.body.lastName){
        // try to find a document with the given email in the db
        UserModel.findByEmail(req.body.email).then((user) => {
            // if the document does not exist, the given email is unique
            if(!user[0]){
                // check that the password is longer than 5 chars
                if (req.body.password.length > 5){
                    // has been validated validated
                    return next();
                } else {
                    return res.status(400).send({error: "The password is not long enough."});
                }
            } else {
                return res.status(400).send({error: "The email is already in use."});
            }
        })
    } else {
        return res.status(400).send({error: "The request is missing fields."});
    }
}

exports.verifyPatch = (req, res, next) => {
    // if password is present, it needs additional validation
    if (req.body.password) {
        this.checkPassword(req, res, next);
    } else {
        return next();
    }
}