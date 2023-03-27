const stripe = require('stripe')('sk_test_51MpFzYEZflEjXl2QWEoDms2VjNJ05MrxgdDi4V1RzqGh8pf5hFv4zREoiGKl8H5vm7IFnGYHU0EHNmIdXibvDxvA00gQ6iDWYs');
const express = require('express');
const app = express();
app.use(express.static('public'));

const DOMAIN = 'http://localhost:3004';

//post add item to card

//get cart

app.post('/checkout', async (req, res) => {
  line_items = req.body.line_items;
  console.log(line_items)
  const session = await stripe.checkout.sessions.create({
    line_items: [
      {
        price_data: {
            currency: "gbp",
            product_data: {
                name: "test item",
            },
            unit_amount: 1000,
        },
        quantity: 1
      },
      {
        price_data: {
            currency: "gbp",
            product_data: {
                name: "test item 2",
            },
            unit_amount: 1000,
        },
        quantity: 1
      },
      {
        price_data: {
            currency: "gbp",
            product_data: {
                name: "test item 3",
            },
            unit_amount: 1000,
        },
        quantity: 1
      },
    ],
    mode: 'payment',
    success_url: `${DOMAIN}/success.html`,
    cancel_url: `${DOMAIN}/cancel.html`,
  });

  res.redirect(303, session.url);
});

app.listen(3004, () => console.log('Running on port 3004'));