const UserModel = require('../models/users.model');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const fs = require('fs');
var publicKEY  = fs.readFileSync('public.key', 'utf8');

/* 
    This file contains the user logic. 

    It is in charge of hashing paswords, and initialising database changes levaraging the 
    user.models.js file.
*/  

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

 exports.getById = (req, res) => {
    // query db then respond
    UserModel.findById(req.params.userId).then((result) => {
        res.status(200).send(result);
    });
 };

 exports.patchById = (req, res) => {
    // check if the updated field is the password
    // if it is make sure to encrypt before adding to database
    if (req.body.password){
        let salt = crypto.randomBytes(16).toString('base64');
        let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
        req.body.password = salt + "$" + hash;
    }
    UserModel.patchUser(req.params.userId, req.body).then((result) => {res.status(204).send({})});
};

// TO-DO: Deny this request if user privilege is low

exports.list = (req, res) => {
    // set a limit for the amount of users to return
    let limit = req.query.limit && req.query.limit <= 100 ? parseInt(req.query.limit) : 10;
    let page = 0;
    if (req.query) {
        if (req.query.page) {
            req.query.page = parseInt(req.query.page);
            page = Number.isInteger(req.query.page) ? req.query.page : 0;
        }
    }
    UserModel.list(limit, page).then((result) => {
        res.status(200).send(result);
    })
};

// remove a user from the db based on its id
exports.removeById = (req, res) => {
    UserModel.removeById(req.params.userId)
        .then((result)=>{
            // once deleted, respond with code 204
            res.status(204).send({});
        });
 };

exports.getByToken = (req, res) => {

    const token = req.cookies.accessToken.slice(1, -1)

    if(token) {
        try {
            
            // decode toke
            decoded = jwt.decode(token, publicKEY);

            // find the user to which it belongs and return
            UserModel.findById(decoded.aud)
            .then((result) => {
                res.status(201).send(JSON.stringify(result));
            });
            
        } catch (e) {
            return res.status(403).send();
        }
    } else {
        // return unauthorised as there is no token present
        return res.status(401).send();
    }
}