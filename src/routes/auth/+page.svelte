<script lang="ts">
  // import prebuilt components
  import   MainButton from "../../components/mainButton.svelte"
  import  SecondaryButton from "../../components/secondaryButton.svelte"
  import { goto } from '$app/navigation';
  import MediaQuery from "../../MediaQuery.svelte";
  import "@fontsource/manrope";
  import { PUBLIC_AUTH_URL } from "$env/static/public";

  let registerToggle = false;

  // switch between login and register
  function toggle(){
    registerToggle = !registerToggle;
  }

  function validateLogin(email:string, password:string){
    // fetch all form fields
    // notice the ! at emailError and passwordError. This ensures those errors do
    // not return null and the code continues. If null, it will not proceed. 
    var emailInput = document.getElementById("email");
    var emailError = document.getElementById("emailError")!;
    var passwordInput = document.getElementById("password");
    var passwordError = document.getElementById("passwordError")!;

    let proceed = false; 

    // set all styles back to normal as this runs every time a the user presses the register button
    // this is because a field might have previously been marked as incorrect, but then the user fixed the issue.
    emailInput?.classList.add("border-borderColor");
    emailInput?.classList.remove("border-[#f43f5f]");
    emailError.innerText = ""

    passwordInput?.classList.add("border-borderColor");
    passwordInput?.classList.remove("border-[#f43f5f]");
    passwordError.innerText = ""

    proceed = true;

    // check for any issues in the inputs
    if(email.length == 0) {
      // empty field
      emailInput?.classList.remove("border-borderColor");
      emailInput?.classList.add("border-[#f43f5f]");
      emailError.innerText = "This field cannot be blank."
      proceed = false
    } else if (!email.toLowerCase().match(/^\S+@\S+\.\S+$/)) {
      // not valid email format
      emailInput?.classList.remove("border-borderColor");
      emailInput?.classList.add("border-[#f43f5f]");
      emailError.innerText = "The email address entered is not valid."
      proceed = false
    }
    if (password.length == 0) {
      passwordInput?.classList.remove("border-borderColor");
      passwordInput?.classList.add("border-[#f43f5f]");
      passwordError.innerText = "This field cannot be blank."
      proceed = false
    }
    return proceed
  }

  function validateRegister(firstName:string, lastName:string, email:string, password:string, repeatPassword:string){
    // fetch all inputs and <p> which are used as errors
    var passwordInput = document.getElementById("password");
    var passwordError = document.getElementById("passwordError")!;
    var rPasswordInput = document.getElementById("rPassword");
    var rPasswordError = document.getElementById("rPasswordError")!;
    var fNameInput = document.getElementById("firstName");
    var fNameError = document.getElementById("fNameError")!;
    var lNameInput = document.getElementById("lastName");
    var lNameError = document.getElementById("lNameError")!;
    var emailInput = document.getElementById("email");
    var emailError = document.getElementById("emailError")!;

    let proceed = false;

    // set all styles back to normal as this runs every time a the user presses the register button
    // this is because a field might have previously been marked as incorrect, but then the user fixed the issue.
    emailInput?.classList.add("border-borderColor");
    emailInput?.classList.remove("border-[#f43f5f]");
    emailError.innerText = ""

    passwordInput?.classList.add("border-borderColor");
    passwordInput?.classList.remove("border-[#f43f5f]");
    passwordError.innerText = ""

    fNameInput?.classList.add("border-borderColor");
    fNameInput?.classList.remove("border-[#f43f5f]");
    fNameError.innerText = ""

    lNameInput?.classList.add("border-borderColor");
    lNameInput?.classList.remove("border-[#f43f5f]");
    lNameError.innerText = ""

    rPasswordInput?.classList.add("border-borderColor");
    rPasswordInput?.classList.remove("border-[#f43f5f]");
    rPasswordError.innerText = ""
    
    proceed = true

    // check for any issues in the inputs
    if (firstName.length == 0){
      fNameInput?.classList.remove("border-borderColor");
      fNameInput?.classList.add("border-[#f43f5f]");
      fNameError.innerText = "This field cannot be empty."
      proceed = false
    }
    if (lastName.length == 0){
      lNameInput?.classList.remove("border-borderColor");
      lNameInput?.classList.add("border-[#f43f5f]");
      lNameError.innerText = "This field cannot be empty."
      proceed = false
    }
    if(email.length == 0) {
      // empty field
      emailInput?.classList.remove("border-borderColor");
      emailInput?.classList.add("border-[#f43f5f]");
      emailError.innerText = "This field cannot be blank."
      proceed = false
    // use regex to check email format
    } else if (!email.toLowerCase().match(/^\S+@\S+\.\S+$/)) {
      // not valid email format
      emailInput?.classList.remove("border-borderColor");
      emailInput?.classList.add("border-[#f43f5f]");
      emailError.innerText = "The email address entered is not valid."
      proceed = false
    }
    // use regex to check if the password has all of the necessary character types
    if (!password.match(/^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{6,}$/)) {
      // unsecure password
      passwordInput?.classList.remove("border-borderColor");
      passwordInput?.classList.add("border-[#f43f5f]");
      passwordError.innerText = "The password entered is not secure enough. The password needs to; \n • Contain at least one upper case and one lower case letter \n • Contain at least one number \n • Contain at least a special character \n • Be at least 7 characters long"
      proceed = false
    }
    // ensure the password is repeated correctly
    if (password != repeatPassword) {
      rPasswordInput?.classList.remove("border-borderColor");
      rPasswordInput?.classList.add("border-[#f43f5f]");
      rPasswordError.innerText = "The passwords do not match."
      proceed = false
    }
    return proceed
  }

  // this function runs when the login for is submitted using the login button
  async function loginSubmit(e: { target: HTMLFormElement; }) {
    // fetch form fields
    const formData = new FormData(e.target);
    // initialise a variable for the API response
    let result = null

    const data : any = {};
    // for each form field, create new key and assign the correct value inputted
    // by the user
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }

    let email = data.email;
	  let password = data.password;

    if (validateLogin(email, password)){

      //create a request to the Auth API (make sure it is running on your machine to test)
      const res = await fetch(PUBLIC_AUTH_URL + 'login/', {
        method: 'POST',
        credentials: 'include',
        // essential to set the header
        headers: {
          "Content-Type": "application/json",
        },
        // add email and password
        body: JSON.stringify({
          email,
          password
        })
      })

      // wait in the background for API response
      result = await res.json()
      const code = await res.status


      if (code != 201){
        // something else happened apart from logging in
        console.log(result);
        if (result.error){
          // find error <p>
          var serverError = document.getElementById("serverError")!;
          // set the text to the error recieved from the server
          serverError.innerText = result.error
          // set to visible
          serverError.style.display = "block";
        }
      } else {

        // fetch current user
        const res2 = await fetch(PUBLIC_AUTH_URL + 'user/', {
          method: 'GET',
          credentials: 'include',
          headers: {
            "Content-Type": "application/json",
          }
        })

        // wait in the background for API response
        result = await res2.json()

        // check what kind of user has logged in
        if (result.privilegeLevel == 1) {
          goto('/dashboard');
        }
        if (1 < result.privilegeLevel && result.privilegeLevel <= 32) {
          //employee
          console.log('employee')
        }
        if (32 < result.privilegeLevel && result.privilegeLevel <= 1028) {
          goto('/activities');
        }
      }
    
    }
  }

  async function registerSubmit(e: { target: HTMLFormElement; }) {
     // fetch form fields
     const formData = new FormData(e.target);
     // initialise a variable for the API response
    let result = null

    const data : any = {};
    // for each form field, create new key and assign the correct value inputted
    // by the user
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }

    let firstName = data.firstName;
    let lastName = data.lastName;
    let email = data.email;
	  let password = data.password;
    let rPassword = data.rPassword;

    if (validateRegister(firstName, lastName, email, password, rPassword)){

      console.log(JSON.stringify({
          firstName,
          lastName,
          email,
          password
        }))

      //create a request to the Auth API (make sure it is running on your machine to test)
      const res = await fetch(PUBLIC_AUTH_URL + 'users/', {
        method: 'POST',
        // essential to set the header
        headers: {
          "Content-Type": "application/json",
        },
        // add email and password
        body: JSON.stringify({
          firstName,
          lastName,
          email,
          password
        })
      })

      // wait in the background for API response
      result = await res.json()
      const code = await res.status

      if (code != 201){
        // something occured other than successful regstration
        console.log(result);
        if (result.error){
          // find the error <p>
          var serverError = document.getElementById("serverError")!;
          // set the text to the error revieved from the server
          serverError.innerText = result.error
          // set to visible
          serverError.style.display = "block";
        }
      } else {
        // if registration was successful change to login ui
        toggle()
      }
    }
  }
</script>

<MediaQuery query="(max-width: 500px)" let:matches>
  <!--if mobile-->
	{#if matches}
  <div class="grid w-screen fontClass h-fill backdrop-blur-sm pb-12 pt-12 px-6">
      <img class="place-self-center pr-3" src = "logo.svg" alt="logo"/>
      <p class="text-center text-3xl font-bold pt-[10%] pb-2">Welcome to cleargym!</p>
      <p class="text-center text-xl font-light pb-[30%]">Lorem ipsum lorem ipsum lerem ipsum</p>

      <!--currently in login UI-->
      {#if registerToggle == false}
      <form on:submit|preventDefault={loginSubmit}>
        <div class="py-2">
          <label for="email">Email</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
          <p id="emailError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>
        <div class="mt-4 pb-[20%]">
          <label for="password">Password</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
          <p id="passwordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>

        <p class="p-3 rounded-md bg-[#f43f5f99] font-semibold" id="serverError" style="display: none;"></p>

        <div class="grid">
          <MainButton type="submit" class="mt-12 w-full max-w-lg place-self-center">Login</MainButton>
        </div>
      </form>

      <div class="grid">
        <div class="inline-flex items-center justify-center w-full">
          <hr class="w-64 h-px my-4 bg-gray-200 border-0">
          <span class="absolute px-3 font-medium text-gray-900 -translate-x-1/2 bg-white left-1/2">or</span>
        </div>
        <!--switch to register UI (line 151 - 177)-->
        <SecondaryButton on:click={() => toggle()} class="place-self-center  w-full max-w-lg ">Register</SecondaryButton>
      </div>
      {:else}
      <form on:submit|preventDefault={registerSubmit}>
        <div class="py-2">
          <label for="firstName">First Name</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="firstName" placeholder="John" name="firstName" value="" />
          <p id="fNameError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>
        <div class="py-2">
          <label for="lastName">Last Name</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="lastName" placeholder="Doe" name="lastName" value="" />
          <p id="lNameError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>
        <div class="py-2">
          <label for="email">Email</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
          <p id="emailError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>
        <div class="py-2">
          <label for="password">Password</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
          <p id="passwordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>
        <div class="py-2">
          <label for="rPassword">Repeat Password</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="rPassword" placeholder="password" name="rPassword" value="" />
          <p id="rPasswordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
        </div>

        <p class="p-3 rounded-md bg-[#f43f5f99] font-semibold" id="serverError" style="display: none;"></p>

        <div class="grid ">
          <MainButton type="submit" class="mt-12  w-3/5 max-w-lg place-self-center">Register</MainButton>
        </div>
      </form>
      {/if}
    </div>
  {:else}
  <div class="min-h-screen h-fill backgroundClass fontClass">
    <div class="grid w-screen h-fill backdrop-blur-sm pb-12 pt-12">
      <div class="grid place-self-center rounded-xl bg-white shadow-lg border-[1px] border-borderColor m-8 px-16 pt-12 pb-8">
        <img class="place-self-center pr-3" src = "logo.svg" alt="logo"/>
        <p class="text-center text-5xl font-bold pt-4">Welcome to cleargym!</p>
        <p class="text-center text-xl font-light pb-20">Lorem ipsum lorem ipsum lerem ipsum</p>

        <!--currently in login UI-->
        {#if registerToggle == false}
        <form on:submit|preventDefault={loginSubmit}>
          <div class="py-2">
            <label for="email">Email</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
            <p id="emailError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>
          <div class="mt-4 pb-8">
            <label for="password">Password</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
            <p id="passwordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>

          <p class="p-3 rounded-md bg-[#f43f5f99] font-semibold" id="serverError" style="display: none;"></p>

          <div class="grid">
            <MainButton type="submit" class="mt-12  w-3/5 max-w-lg place-self-center">Login</MainButton>
          </div>
        </form>

        <div class="grid">
          <div class="inline-flex items-center justify-center w-full">
            <hr class="w-64 h-px my-4 bg-gray-200 border-0">
            <span class="absolute px-3 font-medium text-gray-900 -translate-x-1/2 bg-white left-1/2">or</span>
          </div>
          <!--switch to register UI (line 151 - 177)-->
          <SecondaryButton on:click={() => toggle()} class="place-self-center  w-3/5 max-w-lg ">Register</SecondaryButton>
        </div>
        {:else}
        <form on:submit|preventDefault={registerSubmit}>
          <div class="py-2">
            <label for="firstName">First Name</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="firstName" placeholder="John" name="firstName" value="" />
            <p id="fNameError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>
          <div class="py-2">
            <label for="lastName">Last Name</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="lastName" placeholder="Doe" name="lastName" value="" />
            <p id="lNameError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>
          <div class="py-2">
            <label for="email">Email</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
            <p id="emailError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>
          <div class="py-2">
            <label for="password">Password</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
            <p id="passwordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>
          <div class="py-2">
            <label for="rPassword">Repeat Password</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="rPassword" placeholder="password" name="rPassword" value="" />
            <p id="rPasswordError" class="ml-2 mt-1 text-[#f43f5f] text-sm"></p>
          </div>

          <p class="p-3 rounded-md bg-[#f43f5f99] font-semibold" id="serverError" style="display: none;"></p>

          <div class="grid">
            <MainButton type="submit" class="mt-12  w-3/5 max-w-lg place-self-center">Register</MainButton>
          </div>
        </form>
        {/if}
        

      </div>
    </div>
  </div>
  {/if}
</MediaQuery>

<style>
  .backgroundClass {
    background-image: url("gym.jpg");
    background-size: cover;
  }

  .fontClass {
    font-family: "Manrope";
  }

</style>