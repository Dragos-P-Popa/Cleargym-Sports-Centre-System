let mongoose = require('mongoose');
let mongoConnetionUrl = 'mongodb://127.0.0.1:27017/payments-db'

/*
  This file connects to the MongoDB instance running on the host machine.
*/

mongoose.connect(mongoConnetionUrl, {useNewUrlParser: true});
mongoose.set("strictQuery", false);
// disable so we can cross populate from different tables
mongoose.set("strictPopulate", false);

class Mongo {
  constructor(){
    this.conn = mongoose.connection;
    this.Schema = mongoose.Schema;
  }

  getConnection(){
    return this.conn;
  }

  getSchema(){
    return this.Schema;
  }
}

module.exports = new Mongo();