const conn = require('../mongo').getConnection();
const Schema = require('../mongo').getSchema();

// define the standard user schema for the mongoDB database
const basketSchema = new Schema({
    items: [{ type: Schema.Types.ObjectId, ref: 'items' }],
    userId: String
})

// assign this schema to the 'Users' model
const Basket = conn.model('basket', basketSchema);

exports.createBasket = (basketData) => {
  const basket = new Basket(basketData);
  return basket.save();
}

exports.findByUID = async (userId) => {
  const result = await Basket.findOne({ userId: userId }).populate('items');
  return result;
}

exports.removeByUID = async (userId) => {
  const result = await Basket.deleteMany({userId: userId});
  return result
}