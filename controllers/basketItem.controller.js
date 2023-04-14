const BasketItem = require('../models/basketItem.model')
const Basket = require('../models/basket.model')

// add basketItem to basket
exports.addBasketItem = (req, res) => {
    // create new basketItem
    const basketItem = new BasketItem();

    // set all data
    basketItem.userId = req.params.userId;
    basketItem.facilityId = req.body.facilityId;
    basketItem.activityId = req.body.activityId;
    basketItem.createDate = req.body.createDate;
    basketItem.bookingDate = req.body.bookingDate;
    basketItem.bookingTime = req.body.bookingTime;
    basketItem.bookingLength = req.body.bookingLength;
    basketItem.bookingEndTime = req.body.bookingEndTime;
    basketItem.bookingType = req.body.bookingType;
    basketItem.save()
      .then((result) => {
        // change to cookie
        console.log(req.params.userId)

        // find user basket
        Basket.findByUIDClean(req.params.userId)
        .then(async (basket) => {
          if (!basket) {
            // if not found, this is the first item added to the basket
            // create a user basket
            Basket.createBasket({userId: basketItem.userId}).then((newBasket) => {
              newBasket.items.push(basketItem);
              newBasket.save();
              res.json({ message: 'Item added!' });
            })
          } else {
            // add basketItem to basket
            basket.items.push(basketItem);
            basket.save();
            res.json({ message: 'Item added!' });
          }
        });
      })
};