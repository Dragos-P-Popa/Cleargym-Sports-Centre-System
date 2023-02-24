var Mongoose = require('mongoose').Mongoose;
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

/* 
    This files defines the blacklist DB Schema and manages all DB communication with the blacklist DB. 

    It exports some modules which can be used by other parts of the application to complete
    different operations on the database, either read or write. 
*/  

var blacklistInstance = new Mongoose();

blacklistInstance.set("strictQuery", false);

// connect to a locally hosted mongoDB database
blacklistInstance.connect('mongodb://127.0.0.1:27017/blacklist-db').then(() => {
    console.log("Successfully connected to blacklist database");
  })
  .catch((error) => {
    console.log("Failed to connect to DB");
    console.error(error);
    process.exit(1);
  });

// define the standard blacklist schema
const blacklistSchema = new Schema({
    audience: String,
    refreshToken: String
})

// assign this schema to the 'Blacklist' model
const BlacklistedToken = blacklistInstance.model('Blacklist', blacklistSchema);

// code that adds a given token to the blacklist db
exports.blacklistToken = (tokenData) => {
    const token = new BlacklistedToken(tokenData);
    return token.save();
};

exports.findByToken = (token) => {
    // find blacklist entry in mongo db using the token
    return BlacklistedToken.find({refreshToken: token});
};