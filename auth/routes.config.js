const AuthController = require('./controllers/authentification.controller');
const VerificationMiddleware = require('./middlewares/verification.user.middleware');
const ValidationMiddleware = require('../auth/middlewares/validation.user.middleware');
const BlacklistMiddleware = require('../auth/middlewares/blacklist.token.middleware');

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
        BlacklistMiddleware.isBlacklisted,
        ValidationMiddleware.checkRefresh
    ])
    app.post('/logout', [
        // check the status of the token
        BlacklistMiddleware.isBlacklisted,
        // if not blacklisted, blacklist
        AuthController.logout
    ])
};