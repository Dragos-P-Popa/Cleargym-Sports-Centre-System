<script lang="ts">
  // import prebuilt components
  import   MainButton from "../../components/mainButton.svelte"
  import  SecondaryButton from "../../components/secondaryButton.svelte"
  import "@fontsource/manrope";

  // this function runs when the login for is submitted using the login button
  async function onSubmit(e: { target: HTMLFormElement; }) {
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

    //create a request to the Auth API (make sure it is running on your machine to test)
    const res = await fetch('http://localhost:3001/login/', {
			method: 'POST',
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
      console.log(result);
    } else {
      localStorage.setItem('accessToken', result.accessToken);
      localStorage.setItem('refreshToken', result.refreshToken);

      console.log(localStorage.getItem('accessToken'));
      console.log(localStorage.getItem('refreshToken'));
    }
		

  }
</script>

<div class="grid rounded-xl bg-white shadow-lg border-[1px] border-borderColor m-8 mx-[30%] max-w-[40%] px-16 pt-12 pb-8">
  <img class="place-self-center pr-3" src = "logo.svg" alt="logo"/>
  <p class="text-center text-5xl font-bold pt-4">Welcome to cleargym!</p>
  <p class="text-center text-xl font-light pb-20">Lorem ipsum lorem ipsum lerem ipsum</p>

  <form on:submit|preventDefault={onSubmit}>
    <div>
      <label for="email">Email</label> <br>
      <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
    </div>
    <div class="mt-4 pb-8">
      <label for="password">Password</label> <br>
      <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
    </div>

    <div class="grid">
      <MainButton type="submit" class="mt-12 max-w-lg place-self-center">Login</MainButton>
    </div>
  </form>

  <div class="grid">
    <div class="inline-flex items-center justify-center w-full">
      <hr class="w-64 h-px my-4 bg-gray-200 border-0">
      <span class="absolute px-3 font-medium text-gray-900 -translate-x-1/2 bg-white left-1/2">or</span>
    </div>
    <SecondaryButton class="place-self-center max-w-lg ">Register</SecondaryButton>
  </div>

</div>


<style lang="postcss">
  :global(body) {
    background-image: url("gym.jpeg");
    padding-top: 5rem;
    font-family: "Manrope";
    }
</style>