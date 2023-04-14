const conn = require('../mongo').getConnection();
const Schema = require('../mongo').getSchema();

// define the standard user schema for the mongoDB database
const basketSchema = new Schema({
    items: [{ type: Schema.Types.ObjectId, ref: 'items' }],
    userId: String
})

// assign this schema to the 'Users' model
const Basket = conn.model('basket', basketSchema);

// calculate wether the basket should contain a discount
const discountCalculation = async (basket) => {
  for (let i = 0; i < basket.items.length; i++) {
    // instantiate 2 dates, from current booking's date to 7 days in the future
    let date = new Date(basket.items[i].bookingDate);
    let date2 = new Date(basket.items[i].bookingDate);
    date2.setDate(date.getDate() + 7)

    let count = 0;

    // count the number of bookings which occur in this date range
    for (let k = 0 + i; k < basket.items.length; k++) {
      let date3 = new Date(basket.items[k].bookingDate);
      if (date3.getTime() < date2.getTime() && date3.getTime() > date.getTime()){
        count += 1
        if (count >= 2) {
          // if the threshold for discount has been reached, return 
          return true
        }
      }
    }
  }
  
  return 0
}

// create new DB entry
exports.createBasket = (basketData) => {
  const basket = new Basket(basketData);
  return basket.save();
}

// query DB to find basket by ID
exports.findByUID = async (userId) => {
  let basket = await Basket.findOne({ userId: userId }).populate('items');
  let prices = []

  // fetch all activites
  const res3 = await fetch('http://cleargym.live:3003/activities', {
    method: 'GET'
  })

  let activities = await res3.json();

  try {
    for (let i = 0; i < basket.items.length; i++) {
      for (let k = 0; k < activities.length; k++) {
        if (basket.items[i].activityId == activities[k].activityId){
          
          prices.push(activities[k].price * basket.items[i].bookingLength[1])

          basket = JSON.stringify(basket)
          basket = JSON.parse(basket)
          // append price to the basket data
          // this will be used later to initiate a checkout session
          basket.prices = prices
        }
      }
    }

    await discountCalculation(basket).then((discount) => {
      basket = JSON.stringify(basket)
      basket = JSON.parse(basket)
      // apply discount if discountCalculation() has returned true
      basket.discount = discount
    });

  } catch (error) {
    return basket
  }

  return basket;
}

// same as findByUID but without prices
exports.findByUIDClean = async (userId) => {
  let basket = await Basket.findOne({ userId: userId }).populate('items');
  return basket;
}

exports.getBasketDiscount = async (userId) => {
  let basket = await Basket.findOne({ userId: userId }).populate('items');
  let countMax;

  for (let i = 0; i < basket.items.length + 1; i++) {
    if (i == basket.items.length + 1){
      if (countMax >= 3){
        return true
      } else {
        return false
      }
    }

    let date = new Date(basket.items[i].bookingDate);
    date.setDate(date.getDate() + 7)

    let count = 0;

    for (let k = 0 + i; k < basket.items.length; k++) {
      let date2 = new Date(basket.items[k].bookingDate);
      if (date2 <= date){
        count += 1
      }
    }
    countMax = Math.max(count, countMax)
  }
}

// delete all baskets where ID matches
exports.removeByUID = async (userId) => {
  const result = await Basket.deleteMany({userId: userId});
  return result
}