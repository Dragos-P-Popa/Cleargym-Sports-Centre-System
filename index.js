const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 5001;                  //Port that the node app will be listening to

app.get('/', (req, res) => {        //GET requests to the root ("/") will route here
    console.log(`Request recieved`); 
});

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});