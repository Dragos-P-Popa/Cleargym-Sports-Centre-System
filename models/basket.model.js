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
  let basket = await Basket.findOne({ userId: userId }).populate('items');
  let prices = []

  const res3 = await fetch('http://cleargym.live:3003/activities', {
    method: 'GET'
  })

  let activities = await res3.json();

  for (let i = 0; i < basket.items.length; i++) {
    for (let k = 0; k < activities.length; k++) {
      if (basket.items[i].activityId == activities[k].activityId){
        
        prices.push(activities[k].price * basket.items[i].bookingLength[1])

        basket = JSON.stringify(basket)
        basket = JSON.parse(basket)
        basket.prices = prices
      }
    }
  }

  return basket;
}

exports.removeByUID = async (userId) => {
  const result = await Basket.deleteMany({userId: userId});
  return result
}