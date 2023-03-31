<script lang="ts">
  import "@fontsource/manrope";
  import BookingTypeToggle from "../../../components/bookingTypeToggle.svelte";
  import Calendar from "../../../components/calendar.svelte";
  import EmployeeBooking from "../../../components/employeeBooking.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";
  import ActivityCard from "../../../components/activityCard.svelte";

  import {
    PUBLIC_BOOKINGS_URL,
    PUBLIC_FACILITIES_URL,
  } from "$env/static/public";

  export let data;
  let selectedDate: Date;
  export let selectedMonth: number;
  export let selectedDay: number;
  let user = data.user;
  let selection = 1;
  let available_times;
  let facility_activities;
  let available_activities: any[] = [];

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

  async function activityLoading() {
    /* This function is responsible for validating which activities are available
  at a given facility */
    /*
    // fetch all facilities
    const res1 = await fetch(`http://cleargym.live:3003/facilities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // this data is used to populate the facility selection UI element (line 97-112)
    facilities = await res1.json()*/

    // fetch all activities for a given facility
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
    // fetch all available times for the selected day
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
          {#each available_activities as activity}
            <ActivityCard
              class="my-3"
              heading={activity.activityType}
              location="Studio"
              startTime={activity.activityStartTime}
              sessionLength="1"
            />
          {/each}
        {/await}
      {/if}
    {/if}

    <!-- <div class="flex flex-col">
      <BookingTypeToggle bind:selection />
      {#if selection == 1}
        <EmployeeBooking />
      {:else}
        <p>selection 2</p>
      {/if}
    </div> -->
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
