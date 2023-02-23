const AuthController = require('./controllers/authentification.controller');
const VerificationMiddleware = require('./middlewares/verification.user.middleware');
const ValidationMiddleware = require('../auth/middlewares/validation.user.middleware');

exports.routesConfig = function (app) {
    app.post('/login', [
        // check that email and password
        VerificationMiddleware.isMatch,
        // if correct, create JWT token
        AuthController.login
    ]);
    // endpoint for refreshing access token
    // using a valid refresh token
    app.post('/refresh', [
        ValidationMiddleware.checkRefresh
    ])
};