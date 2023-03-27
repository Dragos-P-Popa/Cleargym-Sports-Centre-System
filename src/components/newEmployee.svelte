<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import { PUBLIC_AUTH_URL } from '$env/static/public'

    let facilities;

    async function addEmployee(e: { target: HTMLFormElement; }) {  
      // fetch form fields
      const formData = new FormData(e.target);
      // initialise a variable for the API response
      let result = null

      const data : any = {};
  
      // for each form field, update the activity object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        data[key] = value;
      }

      let firstName = data.firstName;
      let lastName = data.lastName;
      let email = data.email;
      let password = data.password;
  
      const res = await fetch(PUBLIC_AUTH_URL + 'users', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          firstName,
          lastName,
          email,
          password
        }),
      });
  

      if (res.status == 200) {
        alert('Activity added successfully!');
      } else {
        alert('Error adding activity.');
      }
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
</script>
  
<!-- Add activity -->
<div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Add Employee</p>
    <p class="font-light text-md text-[#515151] text-center">Add a new employee.</p>
  
    <hr class="m-6 mx-24 rounded bg-borderColor">
  
    <form on:submit|preventDefault={addEmployee}>
      <div class="py-2">
        <label for="firstName">First Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="firstName" name="firstName" placeholder="John" value="" />
      </div>
      <div class="py-2">
        <label for="lastName">Last Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="lastName" name="lastName" placeholder="Doe" value="" />
      </div>
      <div class="py-2">
        <label for="email">Email</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
      </div>
      <div class="py-2">
        <label for="password">Password</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
      </div>
      <div class="grid">
        <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Add</MainButton>          
      </div>
    </form>
</div>