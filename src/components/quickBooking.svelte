<script lang="ts">
    import MainButton from "./mainButton.svelte"

    function formatDate(date : number) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2) 
          month = '0' + month;
      if (day.length < 2) 
          day = '0' + day;

      return [year, month, day].join('/');
  }

    async function createBooking(e: { target: HTMLFormElement; }) {
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
      
      // TO:DO - Automatic variables
      let userId = localStorage.getItem("uid");
      let facilitiesId = "1";

      let createDate = formatDate(Date.now());
      let bookingDate = formatDate(Date.parse(data.date));
      let bookingTime = data.time;
      let bookingLength = data.length;
      let bookingType = "General";
      let teamEvent = false;

      //create a request to the Auth API (make sure it is running on your machine to test)
      const res = await fetch('http://localhost:3002/booking', {
        method: 'POST',
        // essential to set the header
        headers: {
          "Content-Type": "application/json",
        },
        // add email and password
        body: JSON.stringify({
          userId,
          facilitiesId,
          createDate,
          bookingDate,
          bookingTime,
          bookingLength,
          bookingType,
          teamEvent
        })
      })

      // wait in the background for API response
      result = await res.json()
      const code = await res.status

      console.log(result);
  }

</script>

<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Quick booking</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new booking at one of our facilities.</p>

    <hr class="m-6 mx-24 rounded bg-borderColor">


    <div class="border-[1px] mb-4 select-none border-borderColor divide-borderColor rounded-lg shadow-sm divide-y">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <p class="p-2 hover:bg-silver ">Swimming pool</p> 
        <p class="p-2 hover:bg-silver ">Gym</p>
        <p class="p-2 hover:bg-silver ">Climbing wall</p>
    </div>

    <form on:submit|preventDefault={createBooking}>
        <div class="py-2">
            <label for="date">Date</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="date" id="date" name="date" value="" />
        </div>
        <div class="py-2">
          <label for="time">Time</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="" />
        </div>
        <div class="py-2">
          <label for="length">Length</label> <br>
          <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
            <option value="01:00">1 hour</option>
            <option value="02:00">2 hours</option>
          </select>
        </div>
    
        <div class="grid">
          <MainButton type="submit" class="mt-12  w-4/5 place-self-center">Checkout</MainButton>
        </div>
      </form>
</div>