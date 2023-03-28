let mongoose = require('mongoose');
let mongoConnetionUrl = 'mongodb://127.0.0.1:27017/payments-db'

mongoose.connect(mongoConnetionUrl, {useNewUrlParser: true});
mongoose.set("strictQuery", false);
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