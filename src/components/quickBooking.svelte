<script lang="ts">
  import MainButton from "./mainButton.svelte"
  //import { selectedMonth, selectedDay } from "../routes/bookings/+page.svelte";
  import { PUBLIC_BOOKINGS_URL, PUBLIC_FACILITIES_URL, PUBLIC_PAYMENTS_URL } from '$env/static/public'
  
  // The values representing the date selected by the user.
  export let selectedDate: Date;
  export let selectedMonth: number;
  export let selectedDay: number;

  let facilities: {
    /* Declaring the property 'facilityName' to prevent the error
       Property 'facilityName' does not exist on type '{ id: any; }'. */
    facilityName: any; id: any; 
  }[];

  // The index of the facility selected by the user.
  let selectedFacility : number;
  // The array of available times for the selected facility.
  let available_times : any[] = [];
     
  // This variable controls whether the confirmation message should be displayed.
  // It is set to 'false' by default.
  let display_confirm = false

  /**
   * Formats the date to YYYY/MM/DD format.
   * 
   * @param {Date} date - The date to format.
   * @param {string} char - The character to use to separate the date.
   * @returns {string} - The formatted date.
  */
  function formatDate(date : Date, char : string) {
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

    return [year, month, day].join(char);
  }

  /**
   * Formats the time to HH:MM format.
   * 
   * @param {number} time - The time to format.
   * @returns {string} - The formatted time.
   */
  function formatTime(time : number) {          
    // converts time from a double digit number to HH:MM format
    var t = time.toString();

    var hour = t
    var min = "00"

    return [hour, min].join(':');
  }
      
  /**
   * Creates a new booking by sending a request to the server 
   * with the user's booking information.
   *
   * @param {Event} e - The form submission event.
   * @returns {Promise<void>} - A Promise that resolves when the booking is created or errors.
   */
  async function createBooking(e: Event) {
    // prevent the form from submitting prior to executing this logic
    e.preventDefault();
  
    // Convert the event's target to an HTML form element
    const form = e.target as HTMLFormElement;

    // fetch form fields
    const formData = new FormData(form);

    // initialise a variable for the API response
    let result = null

    const data : any = {};
    // for each form field, create new key and assign the correct value inputted
    // by the user
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }
    
    // Assign the values from the form to the variables
    let userId = localStorage.getItem("uid");
    let facilityId = facilities[selectedFacility].id;
    let bookingDate = formatDate(selectedDate, '/');
    let bookingTime = data.time;
    let bookingLength = data.length;
    let bookingEndTime = calculateEndTime(bookingTime, bookingLength);

    //create a request to the Auth API (make sure it is running on your machine to test)
    const res = await fetch(PUBLIC_PAYMENTS_URL + `basket/`+userId, {
      method: 'POST',
      // essential to set the header
      headers: {
        "Content-Type": "application/json",
      },
      // convert the data to JSON
      body: JSON.stringify({
        userId,
        facilityId: facilityId,
        activityId: 1,
        bookingDate,
        bookingTime,
        bookingLength,
        bookingEndTime,
      })
    })

    // wait in the background for API response
    result = await res.json()
    const code = await res.status

    // If the code returned from the Bookings API was 200
    if (res.status == 200)
    {
      // Set the 'display_confirm' value to 'true'
      display_confirm = true;
    }

    // Reset the input fields in case a user wishes to make another booking
    form.reset();
  }

  /**
   * Calculates the booking end time by adding the booking time and booking length.
   * 
   * @param {string} bookingTime - The booking time.
   * @param {string} bookingLength - The booking length.
   * @returns {string} - The booking end time.
  */
  function calculateEndTime(bookingTime : string, bookingLength : string) {
    // convert 'bookingTime' and 'bookingLength' to integers
    let bookTime = parseInt(bookingTime)
    let bookLength = parseInt(bookingLength)

    // add 'bookingTime' and 'bookingLength' to get the 'bookingEndTime'
    let combinedTime = bookTime + bookLength

    // Convert the 'combinedTime' to a string and assign it to 'bookingEndTime'
    let bookingEndTime = combinedTime.toString() + ":00"

    // Return the 'bookingEndTime'
    return bookingEndTime
  }

  // If the 'selectedDate' variable is not null
  $: {
    if (selectedDate) {
    // Convert the 'selectedDate' variable to a Date object
    let date = new Date(selectedDate);
    // Assign the month and day to the 'selectedMonth' and 'selectedDay' variables
    selectedMonth = date.getMonth() + 1;
    selectedDay = date.getDate();
    }
  }

  /**
   * Loads the facilities from the Bookings API.
   * 
   * @returns {Promise<Array<any>>} - A Promise that resolves with an array 
   *                                  containing the facilities when they are loaded.
   */
  async function facilityLoading() {
    // fetch all facilities
    const res = await fetch(PUBLIC_FACILITIES_URL + `facilities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })

    // this data is used to populate the facility selection UI element (line 97-112)
    facilities = await res.json()
    return facilities
  }


  /**
   * Loads the available activity times for a selected facility.
   * 
   * @param {number} facilityId - The facility ID.
   * @returns {Promise<Array<any>>} - A Promise that resolves with an array 
   *                                  containing the available times when they are loaded.
  */
  async function timeLoading(facilityId : number) {    
    // fetch all available times for the selected day
    const res3 = await fetch(
      PUBLIC_BOOKINGS_URL + `availability/${facilityId}/${selectedMonth}/${selectedDay}`, {
      method: 'GET',
      headers: {
          "Content-Type": "application/json",
      }
    })

    // The data returned by get_daily_availability() endpoint in the Bookings API
    available_times = await res3.json() 
    return available_times
  }
</script>

<div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
  <p class="text-4xl text-center text-[#1A1A1A]">Quick Booking</p>
  <p class="font-light text-md text-[#515151] text-center">
    Create a new booking at one of our facilities.
  </p>

  <hr class="m-6 mx-24 rounded bg-borderColor">
  <!-- When the form is submitted, call the createBooking() function -->
  <form on:submit={createBooking}>
    <div class="py-2">
      <label for="date">Date</label> <br>
      <input 
        class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" 
        type="date" 
        id="date" 
        name="date" 
        bind:value={selectedDate} 
      />
    </div>

    <div 
    class="border-[1px] mt-4 h-28 overflow-auto mb-4 select-none border-borderColor 
          divide-borderColor rounded-lg shadow-sm divide-y" 
    style="height: 7.8rem;">
      <!--call facilityLoading and wait for API response. While waiting display "loading..."-->
      {#await facilityLoading()}
        <p class="m-5">loading...</p>
      <!--when response is recieved, load data into the html-->
      {:then facilities}
        <!--create new div for each facility-->
        {#each facilities as facility, i}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <div 
            on:click={() => selectedFacility = i} 
            class="flex justify-between hover:bg-silver"
          >
            <p class="p-2 h-10">{facility.facilityName}</p> 
            {#if selectedFacility == i}
              <!--if a facility is selected by clicking on it, display a checkmark icon-->
              <svg 
                class="self-center mr-2" 
                width="24" 
                height="24" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 
                     2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z" 
                  stroke="#106EA2" 
                  stroke-width="1.5" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M7.75 12L10.58 14.83L16.25 9.17" 
                  stroke="#106EA2" 
                  stroke-width="1.5" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
            {/if}
          </div>
        {/each}
      {/await}
    </div>

    <div class="py-2">
      <label for="time">Time</label> <br>
      <!-- If a facility and date have been selected, call the timeLoading() function
           and wait for API response. While waiting display "loading..."-->
      {#if selectedFacility !== undefined && selectedDate !== undefined}
        {#await timeLoading(selectedFacility + 1)}
        <p class="m-5">loading...</p>
        {:then available_times}
          <select 
            class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 
                   shadow-sm min-w-full" 
            name="time" 
            id="time"
          >
            <!-- Format each availabe time to display as "HH:MM" and display it
                as a selectable option -->
            {#each available_times as time}
              <option value={formatTime(time.Hour)}>{time.Hour + ":00"}</option>
            {/each}
          </select>
        {/await}                    
      {/if}
    </div>
    <div class="py-2">
      <!-- Allow the user to choose the amount of time 
           they wish to book an activity for-->
      <label for="length">Length</label> <br>
      <select 
        class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 
               shadow-sm min-w-full" 
        name="length" 
        id="length"
      >
        <option value="01:00">1 hour</option>
        <option value="02:00">2 hours</option>
      </select>
    </div>

    <div class="grid">
      <!-- When the button is clicked, add the items to the basket -->
      <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Checkout</MainButton>          
    </div>
  </form>

  <!-- If the request was successful, display a confirmation message -->
  {#if display_confirm==true}
    <p class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
       style="font-size: 20px; color: green;">
       The booking was successfully added to the basket!
    </p>
  {/if}
</div>
