<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../components/navbar.svelte"
  import BookingCard from "../../components/bookingCard.svelte"
  import ActivityCard from "../../components/activityCard.svelte"
  import BookingInfo from "../../components/viewBooking.svelte"
  import NewBooking from "../../components/newBooking.svelte"
  import Calendar from "../../components/calendar.svelte"
  import Toggle from "../../components/bookingTypeToggle.svelte"
  import { PUBLIC_BOOKINGS_URL, PUBLIC_FACILITIES_URL } from "$env/static/public";

  // Data fetched from server-side-rendering (SSR)
  export let data;
  // Data related to facilities, activities and their availability
  let facilities: any[];
  let available_times;
  let facility_activities;
  let available_activities: any[] = [];

  // Data about bookings amd the user
  export let bookings = data.bookings;
  let user = data.user;
  // Set the iterator 'i' to -1 by default
  let i = -1;

  // These variables are used to store the date selected by the user
  export let selectedDate:Date;
  export let selectedMonth:number;
  export let selectedDay:number;

  /* The 'selection' value is used to determine whether to show 
  General use bookings or activities */
  let selection:number = 1;

  /**
   * Formats the date to YYYY/MM/DD format.
   * 
   * @param {Date} date - The date to format.
   * @returns {string} - The formatted date.
   */
  function formatDate(date : number) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2) {
        month = '0' + month;
      }
          
      if (day.length < 2) {
        day = '0' + day;
      }
          
      return [year, month, day].join('-');
    }

  /**
   * Formats the time to HH:MM format.
   * 
   * @param {number} time - The time to format.
   * @returns {string} - The formatted time.
   */
  function formatTime(time : number) {
    // converts time from a double digit number to HH:MM format
    var hour = time.toString();

    if (hour.length < 2) {
        hour = "0" + hour;
    } 

    var min = "00"

    return [hour, min].join(':');
  }

  /**
   * This function is responsible for setting the focus of the view to a specific booking.
   * 
   * @param {number} id - The id of the booking to focus on.
   * @returns {void}
   */
  function setViewFocus(id : number) {
    // If bookings exist
    if (bookings) {
      /* Set the focus to the booking in a list shown in reverse order.
         This is so that newer bookings are shown at the top. */
      i = bookings.length - 1 - id;
    // Otherwise, i is set to -1
    } else {
      i = -1;
    }
  }

  // Clear the available activities array when a new date is selected
  $: if (selectedDate) {
    available_activities = [];
  }

  /* If the user selected a booking date, and it was assigned to the
      'selectDate' variable, update 'selectedMonth' and 'selectedDay'
      values to match the user's choice. The months and days start at 0,
      hence the '+1' at the end. */
  $: if (selectedDate) {
    selectedMonth = selectedDate.getMonth() + 1;
    selectedDay = selectedDate.getDay() + 1;
  }

  /**
   * This function is responsible for validating which exercise classes are available.
   * 
   * @returns {Promise<any[]>} - The available activities.
   */
  async function activityLoading() {
    // Fetch all activities for the Studio facility
    const res2 = await fetch(
      PUBLIC_FACILITIES_URL + `facilities/7/activities`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
        }
    })
    // The data returned by get_all_activities() endpoint in the Bookings API
    facility_activities = await res2.json()

    // Fetch all available times for the selected day
    const res3 = await fetch(
      PUBLIC_BOOKINGS_URL + `availability/7/${selectedMonth}/${selectedDay}`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
        }
    })
    // The data returned by get_daily_availability() endpoint in the Bookings API
    available_times = await res3.json()

    // Iterate over the arrays of activities and available times
    for (let i = 0; i < facility_activities.length; i++) {
      for(let j = 0; j < available_times.length; j++) {
        /* If the activity's start time matches the available time, 
           add it to the array of available activities */
        if (facility_activities[i].activityStartTime
            == formatTime(available_times[j].Hour)) {
          available_activities.push(facility_activities[i])
        }
      }
    }

    return available_activities
	}

  /**
   * Loads the facilities from the Facilities API.
   * 
   * @returns {Promise<Array<any>>} - A Promise that resolves with an array 
   *                                  containing the facilities when they are loaded.
   */
  async function facilityLoading() {
    // fetch all facilities
    const res1 = await fetch(`http://cleargym.live:3003/facilities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // this data is used to populate the facility selection UI element (line 97-112)
    facilities = await res1.json()
  }

  /**
   * This function is responsible for finding the name of a facility.
   * 
   * @param {number} facilityId - The id of the facility to find.
   * @returns {string} - The name of the facility.
  */
  function findFacilityName(facilityId : number) {
    // Iterate over the array of facilities
    for (let i = 0; i < facilities.length; i++) {
      // If a given 'facilityId' is found, return the facility's name
      if (facilities[i].id == facilityId) {
        return facilities[i].facilityName
      }
    }
  }
</script>

<div class="grid grid-cols-12">
  <!-- Display the navigation bar -->
  <NavBar active=1 firstName={user.firstName} lastName={user.lastName}/>
  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-6">
      <div class="col-span-2">
        <p class="font-bold text-5xl text-[#1A1A1A]">
          Your bookings...
        </p>
        <p class="font-light text-2xl ml-2 text-[#515151]">
          view and manage your bookings
        </p>
        <div class="overflow-y-auto h-[80vh] mt-16">
        <!-- Display all bookings, starting with the latest ones -->
          {#if bookings}
            <!-- slice().reverse() ensures the list of bookings will start 
                 with the highest booking ID at the top-->
            {#each bookings.slice().reverse() as b, i}
              <!-- Display a loading message while the facilities are being fetched -->
              {#await facilityLoading()}
                <p class="m-5">loading...</p>
              {:then}
              <!-- Display a booking card for each booking -->
              <BookingCard on:click={() => setViewFocus(i)}
                class="my-2 transition transform hover:-translate-y-1 
                       motion-reduce:transition-none motion-reduce:hover:transform-none"
                heading="Booking #{b.id}"
                subheading={findFacilityName(b.facilityId)}/>
              {/await}       
            {/each}
          {/if}
        </div>
      </div>
      <div class="col-span-4 px-4 ml-20 mt-12">
        <div class="ml-auto">
          <!--display selected bookings' information-->
          {#if i != -1 && bookings}
            <BookingInfo 
              on:click={()=> i=-1}
              bookingNumber={bookings[i].id}
              bookedOn={bookings[i].createDate}
              bookingDate={formatDate(bookings[i].bookingDate)}
              bookingTime={bookings[i].bookingTime}
              bookingLength={bookings[i].bookingLength}
              facility={findFacilityName(bookings[i].facilityId)}
              activity={bookings[i].activityId}
              user = {user}
            />
          {:else}
          <!--booking creating component-->
          <p class="font-bold text-3xl pb-8 text-[#1A1A1A]">Calendar</p>
          <!-- Display the interactive calendar -->
          <Calendar bind:selectedDate/>
          <!-- If a date was selected, let the user choose the type of booking -->
          {#if selectedDate}
            <div class="grid">
              <div class="justify-self-center pt-6 pb-4">
                <Toggle bind:selection/>
              </div>
            </div>
            <!-- If the user selected a general use booking, display the booking form -->
            {#if selection == 1}
              <NewBooking 
                selectedMonth={selectedMonth} 
                selectedDay={selectedDay} 
                bind:selectedDate
              />
            <!-- If a user selected the exercise class booking, 
                 display the card for each available activity-->
            {:else}
              <!-- Display a loading message while the activities are being fetched -->
              {#await activityLoading()}
                <p class="m-5">loading...</p>
              {:then available_activities}
                <!-- Iterate over the array of available activities -->
                {#each available_activities as activity}
                  <!-- If the activity's day matches the selected date, 
                       display the activity card -->
                  {#if activity.activityDay == 
                       selectedDate.toLocaleString('en-us', {weekday:'long'})}
                    <ActivityCard 
                      class="my-3" 
                      userId = {user._id}
                      facilityId = {7}
                      activityId = {activity.activityId}
                      heading={activity.activityType}
                      location='Studio'
                      bookingDate={selectedDate}
                      bookingTime={activity.activityStartTime}
                      bookingLength="01:00"
                    />
                  {/if}
                {/each}
              {/await}
            {/if}
          {/if}
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
</style>
