<script lang="ts">
  import "@fontsource/manrope";
  import BookingTypeToggle from "../../../components/bookingTypeToggle.svelte";
  import Calendar from "../../../components/calendar.svelte";
  import EmployeeBooking from "../../../components/employeeBooking.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";
  import ActivityCardStaff from "../../../components/activityCardStaff.svelte";

  import {
    PUBLIC_BOOKINGS_URL,
    PUBLIC_FACILITIES_URL,
  } from "$env/static/public";

  // data from the server side
  export let data;

  // data related to facilities, activities and its availability
  let facilities: any[];
  let available_times;
  let facility_activities;
  let available_activities: any[] = [];

  // store the selected date
  let selectedDate: Date;
  export let selectedMonth: number;
  export let selectedDay: number;

  let user = data.user;
  let selection = 1;

  function formatTime(time: number) {
    // converts time from a double digit number to HH:MM format
    var t = time.toString();
    var hour = t;
    var min = "00";
    return [hour, min].join(":");
  }

  function formatDate(date: number) {
    var d = new Date(date),
      month = "" + (d.getMonth() + 1),
      day = "" + d.getDate(),
      year = d.getFullYear();
    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;
    return [year, month, day].join("-");
  }

  // Clear the available activities array when a new date is selected
  $: if (selectedDate) {
    available_activities = [];
  }
  /* If the user selected a booking date, and it was assigned to the
       'selectDate' variable, update 'selectedMonth' and 'selectedDay'
       values to match the user's choice. The months start at 0,
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
      PUBLIC_FACILITIES_URL + `facilities/7/activities`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    // The data returned by get_all_activities() endpoint in the Bookings API
    facility_activities = await res2.json();

    // Fetch all available times for the selected day
    const res3 = await fetch(
      PUBLIC_BOOKINGS_URL + `availability/7/${selectedMonth}/${selectedDay}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    // The data returned by get_daily_availability() endpoint in the Bookings API
    available_times = await res3.json();
    for (let i = 0; i < facility_activities.length; i++) {
      for (let j = 0; j < available_times.length; j++) {
        if (
          facility_activities[i].activityStartTime ==
          formatTime(available_times[j].Hour)
        ) {
          available_activities.push(facility_activities[i]);
        }
      }
    }
    return available_activities;
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
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    // this data is used to populate the facility selection UI element (line 97-112)
    facilities = await res1.json();
  }

  /**
   * This function is responsible for finding the name of a facility.
   *
   * @param {number} facilityId - The id of the facility to find.
   * @returns {string} - The name of the facility.
   */
  function findFacilityName(facilityId: number) {
    // Iterate over the array of facilities
    for (let i = 0; i < facilities.length; i++) {
      // If a given 'facilityId' is found, return the facility's name
      if (facilities[i].id == facilityId) {
        return facilities[i].facilityName;
      }
    }
  }
</script>

<div class="grid grid-cols-12">
  <NavBar active="0" firstName={user.firstName} lastName={user.lastName} />

  <div class="col-span-10 pt-12 px-8">
    <p class="font-bold text-5xl text-[#1A1A1A] w-full pb-10">
      Create a Booking
    </p>
    <Calendar bind:selectedDate />
    {#if selectedDate}
      <div class="grid">
        <div class="justify-self-center pt-6 pb-4">
          <BookingTypeToggle bind:selection />
        </div>
      </div>

      {#if selection == 1}
        <EmployeeBooking bind:selectedDate />
      {:else}
        {#await activityLoading()}
          <p class="m-5">loading...</p>
        {:then available_activities}
          <!-- Iterate over the array of available activities -->
          {#each available_activities as activity}
            <!-- If the activity's day matches the selected date, 
             display the activity card -->
            {#if activity.activityDay == selectedDate.toLocaleString( "en-us", { weekday: "long" } )}
              <ActivityCardStaff
                class="my-3"
                userId={user._id}
                facilityId={7}
                activityId={activity.activityId}
                heading={activity.activityType}
                location="Studio"
                bookingDate={selectedDate}
                bookingTime={activity.activityStartTime}
                bookingLength="01:00"
              />
            {/if}
          {/each}
        {/await}
      {/if}
    {/if}
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
