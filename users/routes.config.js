const UsersController = require('./controllers/users.controller');
const config = require('../index.js');

// expressJS router
exports.routesConfig = function (app) {
    // POST endpoint for the 'users' path
    app.post('/users', [
        // uses the 'insert' function from the users.controller.js file
        UsersController.insert
    ]);
    // get user by Id
    app.get('/users/:userId', [
        UsersController.getById
    ]);
    // update user by Id
    app.patch('/users/:userId', [
        UsersController.patchById
    ]);
    // list users
    app.get('/users', [
        UsersController.list
    ])
    // delete users
    app.delete('/users/:userId', [
        UsersController.removeById
    ])
};