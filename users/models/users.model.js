const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// connect to a locally hosted mongoDB database
mongoose.connect('mongodb://127.0.0.1:27017/auth-db');

// define the standard user schema for the mongoDB database
const userSchema = new Schema({
    firstName: String,
    lastName: String,
    email: String,
    password: String,
    privilegeLevel: Number,
    emailVerified: Boolean
})

// assign this schema to the 'Users' model
const User = mongoose.model('Users', userSchema);

// code that actually adds to the mongodb database
exports.createUser = (userData) => {
    const user = new User(userData);
    return user.save();
};
