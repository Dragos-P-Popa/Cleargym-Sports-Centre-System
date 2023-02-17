const UserModel = require('../models/users.model');
const crypto = require('crypto');

exports.insert = (req, res) => {
    // using 16 random bytes as a salt for the password encryption
    let salt = crypto.randomBytes(16).toString('base64');
    // encrypt password using SHA512 alongside the salt created before
    let hash = crypto.createHmac('sha512',salt)
                                     .update(req.body.password)
                                     .digest("base64");
    // replace plaintext password with encrypted password                                
    req.body.password = salt + "$" + hash;
    // set standard (lowest) permission level
    req.body.privilegeLevel = 1;
    req.body.emailVerified = false;
    UserModel.createUser(req.body)
        .then((result) => {
            res.status(201).send({id: result._id});
        });
 };