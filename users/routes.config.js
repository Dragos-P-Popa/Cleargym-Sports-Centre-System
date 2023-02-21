const UsersController = require('./controllers/users.controller');
const ValidationMiddleware = require('../auth/middlewares/validation.user.middleware');
const VerificationMiddleware = require('../auth/middlewares/verification.user.middleware');

/*
    Defines the app's routes.
*/  

// expressJS router
exports.routesConfig = function (app) {
    // POST endpoint for the 'users' path
    app.post('/users', [
        VerificationMiddleware.verifyUserCreation,
        VerificationMiddleware.checkPassword,
        // uses the 'insert' function from the users.controller.js file
        UsersController.insert
    ]);
    // get user by Id
    app.get('/users/:userId', [
        // user should be logged in to access this
        ValidationMiddleware.checkJWT,
        UsersController.getById
    ]);
    // update user by Id
    app.patch('/users/:userId', [
        // user should be logged in to access this
        ValidationMiddleware.checkJWT,
        VerificationMiddleware.verifyPatch,
        VerificationMiddleware.checkPassword,
        UsersController.patchById
    ]);
    // list users
    app.get('/users', [
        // user should be logged in to access this
        ValidationMiddleware.checkJWT,
        UsersController.list
    ])
    // delete users
    app.delete('/users/:userId', [
        // user should be logged in to access this
        ValidationMiddleware.checkJWT,
        UsersController.removeById
    ])
};