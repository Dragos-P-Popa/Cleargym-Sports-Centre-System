const conn = require('../mongo').getConnection();
const Schema = require('../mongo').getSchema();

// define basketItem schema
// this is the same as the booking api booking schema
const basketItemSchema = new Schema({
    belongsIn: { type: Schema.Types.ObjectId, ref: 'basket' },
    userId: String,
    facilityId: Number,
    activityId: Number,
    createDate: Date,
    bookingDate: String,
    bookingTime: String,
    bookingLength: String,
    bookingEndTime: String,
    bookingType: String
})

const BasketItem = conn.model('items', basketItemSchema);
module.exports = BasketItem;

// find basketItem by ID
exports.findById = (id) => {
  return BasketItem.findById(id).then((result) => {
      result = result.toJSON();
      delete result.__v;
      return result;
  });
};