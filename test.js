//Defining the modules needed for the tests
const mocha = require("mocha");
const supertest = require("supertest");
const should = require("should");
const {application} = require("express");


//Connect to the server
let server = supertest.agent("http://localhost:3001");

//Defining a user id variable to store it and use it in a delete request
let userId;
let authToken;
let refToken;
/*-----------------------------------------------------------------
This section will start showing the tests for each api and try to explain which tests are running on each stage
-------------------------------------------------------------------*/

//Test 1: Create a new user : POST request

describe("Testing",function (){


    it("Create a user",function (done) {
    server
        .post('/users')
        .send({"firstName": "testCase002",
            "lastName": "testCase002",
            "email": "newemail@new.com",
            "password": "Test@case20231"})

        //This means the record has been created
        .expect(201)
        .end(function (err,res){
            res.status.should.equal(201);
            if(res.body.hasOwnProperty('id'))
            {
                userId = res.body.id;

            }
            done();
        });
    });


//Test 2: Bad request: duplicate email

        it("Create a user with duplicate email",function (done) {
            server
                .post('/users')
                .send({"firstName": "testCase002",
                    "lastName": "testCase002",
                    "email": "TestCase2023.10@squad007.com",
                    "password": "Test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                    done();
                });
        });

//Test 3: Bad request: password does not match the password criteria: Capital letter missing


        it("Create a user with weak password - Capital letter missing",function (done) {
            server
                .post('/users')
                .send({"firstName": "testCase002",
                    "lastName": "testCase002",
                    "email": "newMember10@squad007.com",
                    "password": "test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                    done();
                });
        });
//Test 4: Bad request: password does not match the password criteria: small letters missing
        it("Create a user with weak password - small letters missing",function (done) {
            server
                .post('/users')
                .send({"firstName": "testCase002",
                    "lastName": "testCase002",
                    "email": "Newmember11@squad007.com",
                    "password": "T@20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 5: Bad request: password does not match the password criteria: special character missing
        it("Create a user with weak password - small letters missing",function (done) {
            server
                .post('/users')
                .send({"firstName": "testCase002",
                    "lastName": "testCase002",
                    "email": "Newmember12@squad007.com",
                    "password": "Test20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 6:  Bad request: password does not match the password criteria: numbers missing

        it("Create a user with weak password - numbers missing",function (done) {
            server
                .post('/users')
                .send({"firstName": "testCase002",
                    "lastName": "testCase002",
                    "email": "Newmember13@squad007.com",
                    "password": "Test@test"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 7: Bad request: first name missing
        it("Create a user with missing first name",function (done) {
            server
                .post('/users')
                .send({
                    "lastName": "testCase002",
                    "email": "Newmember1133@squad007.com",
                    "password": "Test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 8: Bad request: last name empty
        it("Create a user with empty last name",function (done) {
            server
                .post('/users')
                .send({"firstName": "Myname",
                    "lastName": "",
                    "email": "Newmember1144@squad007.com",
                    "password": "Test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 9: Bad request: last name missing
        it("Create a user with missing last name",function (done) {
            server
                .post('/users')
                .send({"firstName": "MYname",
                    "email": "Newmember1155@squad007.com",
                    "password": "Test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 10: Bad request: missing email
        it("Create a user with missing email",function (done) {
            server
                .post('/users')
                .send({"firstName": "",
                    "lastName": "testCase002",
                    "password": "Test@case20231"})

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 11: Bad request: missing password

        it("Create a user with missing password",function (done) {
            server
                .post('/users')
                .send({"firstName": "",
                    "lastName": "testCase002",
                    "email": "Newmember1166@squad007.com"
                   })

                //This means the record has been created
                .expect(400)
                .end(function (err,res){
                    res.status.should.equal(400);
                        done();
                });
        });

//Test 12: Login with correct credentials
        it("Login a user - correct credentials", function (done) {
            server
                .post('/login')
                .send({
                    "email": "newemail@new.com",
                    "password": "Test@case20231"
                })
                .expect(201)
                .end(function (err, res) {
                    res.status.should.equal(201);
                    if(res.body.hasOwnProperty("accessToken"))
                    {
                        authToken = res.body.accessToken;
                    }
                    if(res.body.hasOwnProperty("refreshToken"))
                    {
                        refToken = res.body.refreshToken;
                    }
                    done();
                });
        });


//Test 13: Refresh and get new access token
        it("Refresh and get a new access token", function (done) {
            server
                .post('/refresh')
                .send({
                    "refreshToken" : refToken,
                    "audience": "newemail@new.com"

                })
                .expect(201)
                .end(function (err, res) {
                    res.status.should.equal(201);
                    if(res.body.hasOwnProperty("accessToken"))
                    {
                        authToken = res.body.accessToken;
                    }
                    done();
                });
        });

//Test 14: Refresh without an audience
        it("Refresh without an audience - unauthorized", function (done) {
            server
                .post('/refresh')
                .send({
                    "refreshToken" : refToken
                })
                .expect(401)
                .end(function (err, res) {
                    res.status.should.equal(401);
                    done();
                });
        });

//Test 15: Refresh with the wrong audience
        it("Refresh with wrong audience - unauthorized", function (done) {
            server
                .post('/refresh')
                .send({
                    "refreshToken" : refToken,
                    "audience" : "wrong@wrong.com"
                })
                .expect(401)
                .end(function (err, res) {
                    res.status.should.equal(401);
                    done();
                });
        });

//Test 16: Refresh without a refresh token
        it("Refresh without refresh token - bad request", function (done) {
            server
                .post('/refresh')
                .send({

                    "audience": "newemail@new.com"
                })
                .expect(400)
                .end(function (err, res) {
                    res.status.should.equal(400);
                    done();
                });
        });

//Test 17: Login with incorrect credentials
          it("Login a user - incorrect credentials", function (done) {
          server
          .post('/login')
           .send({
                "email": "TestCase2023.10@squad007.com",
                "password": "wrongPassword"
            })
          .expect(400)
          .end(function (err, res) {
              res.status.should.equal(400);
              done();
          });
         });

//Test 18: Get the user details by GET request
        it("Get the user details by the user ID", function (done){

            server
                .get('/users/'+userId)
                .auth(authToken, { type: 'bearer' })

                //This means that there is no record of that user which means deletion succeed
                .expect(200)
                .end(function (err,res) {
                    res.status.should.equal(200);
                    done();

                })
        })


//Test 19: update the user details by PATCH request (Password)
        it("Update user details - password",function (done) {

            server
              .patch('/users/'+userId)
              .auth(authToken, { type: 'bearer' })
              .send({
                  "password" : "Zz123456!"
                })

                //This means the record has been updated
              .expect(204)
              .end(function (err,res){
                res.status.should.equal(204);
                done();

                });
        });

//Test 20: update the user details by PATCH request (First name)
        it("Update user details - First name",function (done) {

            server
                .patch('/users/'+userId)
                .auth(authToken, { type: 'bearer' })
                .send({
                    "firstName" : "MyName is A member"
                })

                //This means the record has been updated
                .expect(204)
                .end(function (err,res){
                    res.status.should.equal(204);
                    done();

                });
        });

//Test 21: update the user details by PATCH request (Last name)
        it("Update user details - last name",function (done) {

            server
                .patch('/users/'+userId)
                .auth(authToken, { type: 'bearer' })
                .send({
                    "lastName" : "MyLastname is A programmer"
                })

                //This means the record has been updated
                .expect(204)
                .end(function (err,res){
                    res.status.should.equal(204);
                    done();

                });
        });

//Test 22: update the user details by PATCH request (email)
        it("Update user details - eamil",function (done) {

            server
                .patch('/users/'+userId)
                .auth(authToken, { type: 'bearer' })
                .send({
                    "email" : "jan@jan.com"
                })

                //This means the record has been updated
                .expect(204)
                .end(function (err,res){
                    res.status.should.equal(204);
                    done();

                });
        });

//Test 23: update the user details by PATCH request (All details)
        it("Update user details - all the details",function (done) {

            server
                .patch('/users/'+userId)
                .auth(authToken, { type: 'bearer' })
                .send({
                    "firstName": "All",
                    "lastName": "details",
                    "email": "FEB@Chaged.com",
                    "password": "New@month02"
                })

                //This means the record has been updated
                .expect(204)
                .end(function (err,res){
                    res.status.should.equal(204);
                    done();

                });
        });

//Test 24: Get all the users that has been created if the privilege is high
       it("Get all the users in the Database", function (done){

            server
               .get('/users')
                .auth(authToken, { type: 'bearer' })

                //This means that there is no record of that user which means deletion succeed
               .expect(200)
              .end(function (err,res) {
                  res.status.should.equal(200);
                   done();

               })
        })



//Test 25: Delete the user that has been created
    it("Delete the user by the user ID", function (done){
       server
            .delete('/users/'+userId)
           .auth(authToken, { type: 'bearer' })

            //This means that there is no record of that user which means deletion succeed
        .expect(204)
           .end(function (err,res) {
                res.status.should.equal(204);
               done();

            })
          })



    }

)



