const stripe = require('stripe')('sk_test_51MpFzYEZflEjXl2QWEoDms2VjNJ05MrxgdDi4V1RzqGh8pf5hFv4zREoiGKl8H5vm7IFnGYHU0EHNmIdXibvDxvA00gQ6iDWYs');
const express = require('express');
const app = express();
app.use(express.static('public'));
const BasketItemController = require('./controllers/basketItem.controller')
const BasketModel = require('./models/basket.model')
const cors = require('cors');
require('dotenv').config();

app.use(cors());

// webiste is always running locally, so success/cancel redirects should also be localhost
const DOMAIN = 'http://localhost:5173';

// read json request body
app.use(express.json())

// change discount amount
app.post('/discount/:discount' , (req, res) => {
  process.env.DISCOUNT = req.params.discount;
  res.status(200).send({"discount": process.env.DISCOUNT})
})

// get discount amount
app.get('/discount', (req, res) => {
  res.status(200).send({"discount": process.env.DISCOUNT})
})

// add item to basket
app.post('/basket/:userId', async (req, res) => {
  let items = req.body.items;
  
  // check if user already has a basket
  BasketModel.findByUID(req.body.userId).then((result) => {
      if (!result) {
        // if not, create new basket
        BasketModel.createBasket({userId: req.body.userId})
      }
    });

    // add items to basket
    BasketItemController.addBasketItem(req, res)
})

// get basket
app.get('/basket/:userId', async (req, res) => {
  let prices = [];

  BasketModel.findByUID(req.params.userId)
      .then(async (basket) => {
          res.status(201).send(basket);
      });
})

// clear a user basket (delete)
app.delete('/basket/:userId', async (req, res) => {
  BasketModel.removeByUID(req.params.userId)
      .then((result) => {
        res.status(200).send(result);
      })
})

let facilities = [];
let activities = [];

async function dataLoading() {
  // fetch all facilities
  const res1 = await fetch(`http://cleargym.live:3003/facilities`, {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
    }
  })
  // this data is used to populate the 'facilities' array
  facilities = await res1.json()

  // fetch all activities
  const res2 = await fetch(`http://cleargym.live:3003/activities`, {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
    }
  })
  // this data is used to populate the 'activities' array
  activities = await res2.json()
}


function findFacilityName(facilityId) {
  // Iterate over the array of facilities
  for (let i = 0; i < facilities.length; i++) {
    // If a given 'facilityId' is found, return the facility's name
    if (facilities[i].id == facilityId) {
      return facilities[i].facilityName
    }
  }
}


function findActivityName(activityId) {
  // Iterate over the array of activities
  for (let i = 0; i < activities.length; i++) {
    // If a given 'activityId' is found, return the activity's name
    if (activities[i].activityId == activityId) {
      return activities[i].activityType
    }
  }
}

// create stripe checkout session and redirect
app.post('/checkout/:userId', async (req, res) => {

    // find the users basket
    BasketModel.findByUID(req.params.userId)
    .then(async (basket) => {

      // format user basket items to stripe checkout line items
      let line_items = [];
      let coupon = null;
      let session;

      // check if basket has discount applied
      if (basket.discount == true) {
        coupon = await stripe.coupons.create({percent_off: process.env.DISCOUNT, duration: 'once'});
      }

      // format basket items
      for (let i = 0; i < basket.items.length; i++) {
        
        let product_data = {name: findFacilityName(basket.items[i].facilityId) + " - " + findActivityName(basket.items[i].activityId) + " - " + basket.items[i].bookingDate}
        let price_data = {currency: "gbp", product_data, unit_amount: basket.prices[i] * 100 /*, recurring: { "interval": "month", "interval_count": 1  }*/}
        line_items[i] = {price_data: price_data, quantity: 1}
        
      }    

      // if coupon exists, create a checkout session with a coupon applied
      if (coupon) {
        session = await stripe.checkout.sessions.create({
          // items formatted before
          line_items,
          discounts: [{
            coupon: coupon.id,
          }],
          //mode: 'subscription',
          mode: 'payment',
          // redirect URLs
          success_url: `${DOMAIN}/success`,
          cancel_url: `${DOMAIN}/cancel`,
        });
      } else {
        session = await stripe.checkout.sessions.create({
          line_items,
          //mode: 'subscription',
          mode: 'payment',
          // redirect URLs
          success_url: `${DOMAIN}/success`,
          cancel_url: `${DOMAIN}/cancel`,
        });
      }

      res.redirect(303, session.url);
    });
});

// load activities and facilities
dataLoading();
// debug log when starting module
app.listen(3004, () => console.log('Running on port 3004'));
