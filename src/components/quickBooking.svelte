<script lang="ts">
    import MainButton from "./mainButton.svelte"

    let facilities;
    let selectedFacility : number;

    function formatDate(date : number) {
      // converts date from DateTime to yr/mth/day
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      // if day or month is 1-9 return it as 01-09 instead
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
      
      let userId = localStorage.getItem("uid");
      let facilitiesId = facilities[selectedFacility].id;
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

  async function facilityLoading() {
    // fetch all facilities
		const res = await fetch('http://localhost:3003/facilities', {
			method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
		})

    // this data is used to populate the facility selection UI element (line 97-112)
	  facilities = await res.json()
    return facilities
	}
  
</script>

<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Quick booking</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new booking at one of our facilities.</p>

    <hr class="m-6 mx-24 rounded bg-borderColor">


    <div class="border-[1px] h-28 overflow-auto mb-4 select-none border-borderColor divide-borderColor rounded-lg shadow-sm divide-y">
      <!--call facilityLoading and wait for API response. While waiting display "loading..."-->
      {#await facilityLoading()}
        <p class="m-5">loading...</p>
      <!--when response is recieved, load data into the html-->
      {:then facilities}
        <!--create new div for each facility-->
        {#each facilities as facility, i}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <div on:click={() => selectedFacility = i} class="flex justify-between hover:bg-silver">
            <p class="p-2 h-10">{facility.facilityName}</p> 
            {#if selectedFacility == i}
              <!--if a facility is selected by clicking on it, display a checkmark icon-->
              <svg class="self-center mr-2" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z" stroke="#106EA2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7.75 12L10.58 14.83L16.25 9.17" stroke="#106EA2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            {/if}
          </div>
        {/each}
      {/await}
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