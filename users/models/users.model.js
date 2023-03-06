const mongoose = require('mongoose');
const Schema = mongoose.Schema;

/* 
    This files defines the User DB Schema and manages all DB communication. 

    It exports some modules which can be used by other parts of the application to complete
    different operations on the database, either read or write. 
*/  

mongoose.set("strictQuery", false);

// connect to a locally hosted mongoDB database
mongoose.connect('mongodb://127.0.0.1:27017/auth-db').then(() => {
    console.log("Successfully connected to users database");
  })
  .catch((error) => {
    console.log("Failed to connect to DB");
    console.error(error);
    process.exit(1);
  });

// define the standard user schema for the mongoDB database
const userSchema = new Schema({
    firstName: String,
    lastName: String,
    email: {type: String, unique: true},
    password: String,
    privilegeLevel: Number,
    emailVerified: {type: Boolean, default: false}
})

// assign this schema to the 'Users' model
const User = mongoose.model('Users', userSchema);

// code that actually adds to the mongodb database
exports.createUser = (userData) => {
    const user = new User(userData);
    return user.save();
};

exports.findById = (id) => {
    // find user entry in mongo db using the Id
    return User.findById(id).then((result) => {
        // convert to JSON
        result = result.toJSON();
        // delete uneccessary fields from response
        delete result._id;
        delete result.__v;
        return result;
    });
};

exports.findByEmail = (email) => {
    // find user entry in mongo db using the email
    return User.find({email: email}).then((result) => {
        return result;
    });
};

// mongoDB updating one document
exports.patchUser = (id, userData) => {
    // find document based on given ID and update using userData
    return User.findOneAndUpdate({
        _id: id,
    }, userData);
};

// list users in db
exports.list = (perPage, page) => {
    return new Promise((resolve, reject) => {
        User.find()
            .limit(perPage)
            .skip(perPage * page)
            .exec(function (err, users) {
                if (err) {
                    reject(err);
                } else {
                    resolve(users);
                }
            })
    });
};

// delete users
exports.removeById = (userId) => {
    return new Promise((resolve, reject) => {
        // remove all user documents with matching id
        User.deleteMany({_id: userId}, (err) => {
            if (err) {
                reject(err);
            } else {
                resolve(err);
            }
        });
    });
};