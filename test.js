//Defining the modules needed for the tests
const mocha = require("mocha");
const supertest = require("supertest");
const should = require("should");
const {application} = require("express");


//Connect to the server
let server = supertest.agent("http://localhost:5001");

//Defining a user id variable to store it and use it in a delete request
let userId;

/*-----------------------------------------------------------------
This section will start showing the tests for each api and try to explain which tests are running on each stage
-------------------------------------------------------------------*/

//Test 1: Create a new user : POST request

describe("Testing",function (){

    it("create a user",function (done) {


    server
        .post('/users')
        .send({"firstName": "testCase001",
            "lastName": "testCase001",
            "email": "testcase001@squad007.com",
            "password": "test@case001"})

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

//Test 2: Get the user details by GET request
        it("Get the user details by the user ID", function (done){

            server
                .get('/users/'+userId)

                //This means that there is no record of that user which means deletion succeed
                .expect(200)
                .end(function (err,res) {
                    res.status.should.equal(200);
                    done();

                })
        })



//Test 3: update the user details by PATCH request
        it("Update user details",function (done) {


            server
                .patch('/users/'+userId)
                .send({"firstName": "UpdatedName",
                    "lastName": "testCase001",
                    "email": "testcase001@squad007.com"
                })

                //This means the record has been updated
                .expect(204)
                .end(function (err,res){
                    res.status.should.equal(204);
                    done();
                });
        });
//Test 4: Get all the users that has been created if the privilege is high
        it("Get all the users in the Database", function (done){

            server
                .get('/users')

                //This means that there is no record of that user which means deletion succeed
                .expect(200)
                .end(function (err,res) {
                    res.status.should.equal(200);
                    done();

                })
        })



//Test 5: Delete the user that has been created


    it("Delete the user by the user ID", function (done){

        server
            .delete('/users/'+userId)

            //This means that there is no record of that user which means deletion succeed
            .expect(204)
            .end(function (err,res) {
                res.status.should.equal(204);
                done();

            })
    })



    }

)



