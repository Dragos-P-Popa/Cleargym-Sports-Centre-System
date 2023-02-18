const express = require('express'); //Import the express dependency
const app = express();              //Instantiate an express app, the main work horse of this server
const port = 3001;                  //Port that the node app will be listening to

/* 
    This file is the root of the application.
*/  

// uses the routes defined in the routes.config file
const UsersRouter = require('./users/routes.config');
const AuthRouter = require('./auth/routes.config');

app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Credentials', 'true');
    res.header('Access-Control-Allow-Methods', 'GET,HEAD,PUT,PATCH,POST,DELETE');
    res.header('Access-Control-Expose-Headers', 'Content-Length');
    res.header('Access-Control-Allow-Headers', 'Accept, Authorization, Content-Type, X-Requested-With, Range');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    } else {
        return next();
    }
});

// use JSON in communications
app.use(express.json());
// assigns the current 'app' expressJs instance to the UsersRouter
UsersRouter.routesConfig(app);
// use routes defined in auth/routes.config.js
AuthRouter.routesConfig(app);

app.listen(port, () => {
    console.log(`Now listening on port ${port}`); 
});