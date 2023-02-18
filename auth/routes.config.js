const AuthController = require('./controllers/authentification.controller');
const VerificationMiddleware = require('./middlewares/verification.user.middleware');

exports.routesConfig = function (app) {
    app.post('/login', [
        // check that email and password
        VerificationMiddleware.isMatch,
        // if correct, create JWT token
        AuthController.login
    ]);
};