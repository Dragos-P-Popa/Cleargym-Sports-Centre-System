const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 5001;                  //Port that the node app will be listening to


app.get('/users', (req, res) => {
    res.status(200).json({ action: "list all users" }); 
});

app.post('/users', (req, res) => {
    res.status(200).json({ action: "create new user" }); 
})

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});