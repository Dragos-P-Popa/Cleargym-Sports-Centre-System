const stripe = require('stripe')('sk_test_51MpFzYEZflEjXl2QWEoDms2VjNJ05MrxgdDi4V1RzqGh8pf5hFv4zREoiGKl8H5vm7IFnGYHU0EHNmIdXibvDxvA00gQ6iDWYs');
const express = require('express');
const app = express();
app.use(express.static('public'));
const BasketItemController = require('./controllers/basketItem.controller')
const BasketModel = require('./models/basket.model')
const cors = require('cors');

app.use(cors());

const DOMAIN = 'http://localhost:5173';

app.use(express.json())

//post add item to basket
app.post('/basket/:userId', async (req, res) => {
  let items = req.body.items;
  
  BasketModel.findByUID(req.body.userId).then((result) => {
      if (!result) {
        BasketModel.createBasket({userId: req.body.userId})
      }
    });

    BasketItemController.addBasketItem(req, res)
})

//get basket
app.get('/basket/:userId', async (req, res) => {
  let prices = [];

  BasketModel.findByUID(req.params.userId)
      .then(async (basket) => {
          res.status(201).send(basket);
      });
})

app.delete('/basket/:userId', async (req, res) => {
  BasketModel.removeByUID(req.params.userId)
      .then((result) => {
        res.status(200).send(result);
      })
})

app.post('/checkout/:userId', async (req, res) => {

    BasketModel.findByUID(req.params.userId)
    .then(async (basket) => {

      let line_items = [];
      let coupon;
      let session;

      if (basket.discount) {
        coupon = await stripe.coupons.create({percent_off: basket.discount, duration: 'once'});
      }

      for (let i = 0; i < basket.items.length; i++) {
        
        let product_data = {name: basket.items[i].bookingType + " " + basket.items[i].bookingDate}
        let price_data = {currency: "gbp", product_data, unit_amount: basket.prices[i] * 100}
        line_items[i] = {price_data: price_data, quantity: 1}
        
      }    


      if (coupon) {
        session = await stripe.checkout.sessions.create({
          line_items,
          discounts: [{
            coupon: coupon.id,
          }],
          mode: 'payment',
          success_url: `${DOMAIN}/success`,
          cancel_url: `${DOMAIN}/cancel`,
        });
      } else {
        session = await stripe.checkout.sessions.create({
          line_items,
          mode: 'payment',
          success_url: `${DOMAIN}/success`,
          cancel_url: `${DOMAIN}/cancel`,
        });
      }

      res.redirect(303, session.url);
    });
});

app.listen(3004, () => console.log('Running on port 3004'));
