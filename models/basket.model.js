const conn = require('../mongo').getConnection();
const Schema = require('../mongo').getSchema();

// define the standard user schema for the mongoDB database
const basketSchema = new Schema({
    items: [{ type: Schema.Types.ObjectId, ref: 'items' }],
    userId: String
})

// assign this schema to the 'Users' model
const Basket = conn.model('basket', basketSchema);

const discountCalculation = async (basket) => {
  for (let i = 0; i < basket.items.length; i++) {
    let date = new Date(basket.items[i].bookingDate);
    let date2 = new Date(basket.items[i].bookingDate);
    date2.setDate(date.getDate() + 7)

    let count = 0;

    for (let k = 0 + i; k < basket.items.length; k++) {
      let date3 = new Date(basket.items[k].bookingDate);
      //console.log("date1: "+date)
      //console.log("date3: "+date3)
      //console.log("date2: "+date2 + '\n')
      if (date3.getTime() <= date2.getTime() && date3.getTime() >= date.getTime()){
        count += 1
        //console.log(count)
        if (count >= 2) {
          return 15
        }
      }
    }
  }
  
  return 0
}

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

  try {
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

    await discountCalculation(basket).then((discount) => {
      //console.log(discount)
      basket = JSON.stringify(basket)
      basket = JSON.parse(basket)
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

exports.removeByUID = async (userId) => {
  const result = await Basket.deleteMany({userId: userId});
  return result
}