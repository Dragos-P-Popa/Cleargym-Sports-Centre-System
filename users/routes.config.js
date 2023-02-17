const UsersController = require('./controllers/users.controller');
const config = require('../index.js');

// expressJS router
exports.routesConfig = function (app) {
    // POST endpoint for the 'users' path
    app.post('/users', [
        // uses the 'insert' function from the users.controller.js file
        UsersController.insert
    ]);
};