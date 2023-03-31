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
  
  export let data;
  let facilities;
  let available_times;
  let facility_activities;
  let available_activities: any[] = [];

  // data fetched from server-side-rendering (SSR)
  // +page.ts
  export let bookings = data.bookings;
  let user = data.user;
  let i = -1;

  export let selectedDate:Date;
  export let selectedMonth:number;
  export let selectedDay:number;
  let selection:number = 1;
  
  // format date
  function formatDate(date : number) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2)
          month = '0' + month;
      if (day.length < 2)
          day = '0' + day;

      return [year, month, day].join('-');
    }

  function formatTime(time : number) {
      
      // converts time from a double digit number to HH:MM format
      var t = time.toString();

      var hour = t
      var min = "00"

      return [hour, min].join(':');
  }
  
    // when clicking on bookings in the list (left) this is called.
    // based on 'i' the BookingInfo component will display the appropriate
    // booking info
    function setViewFocus(id : number) {
      i = id
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
    const res2 = await fetch(PUBLIC_FACILITIES_URL + `facilities/7/activities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // The data returned by get_all_activities() endpoint in the Bookings API
    facility_activities = await res2.json()

    // fetch all available times for the selected day
    const res3 = await fetch(PUBLIC_BOOKINGS_URL + `availability/7/${selectedMonth}/${selectedDay}`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // The data returned by get_daily_availability() endpoint in the Bookings API
    available_times = await res3.json()

    for (let i = 0; i < facility_activities.length; i++) {
      for(let j = 0; j < available_times.length; j++) {
        if (facility_activities[i].activityStartTime 
            == formatTime(available_times[j].Hour)) {
          available_activities.push(facility_activities[i])
        }
      }
    }

    return available_activities

	}
</script>

<div class="grid grid-cols-12">
  <NavBar active=1 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
      <div class="grid grid-cols-6">
          <div class="col-span-2">
            <p class="font-bold text-5xl text-[#1A1A1A]">Your bookings...</p>
            <p class="font-light text-2xl ml-2 text-[#515151]">view and manage your bookings</p>

            <div class="overflow-y-auto h-[80vh] mt-16">
              <!--display all bookings-->
              {#each bookings as b, i}
                <BookingCard on:click={() => setViewFocus(i)}
                  class="my-2 transition transform hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none"
                  heading="Booking #{b.id}"
                  subheading={b.bookingType}/>
              {/each}
            </div>

          </div>
          <div class="col-span-4 px-4 ml-20 mt-12">
          <div class="ml-auto">
            <!--display selected bookings' information-->
            {#if i != -1}
              <BookingInfo on:click={()=> i=-1}
                           bookingNumber={bookings[i].id}
                           bookedOn={bookings[i].createDate}
                           bookingDate={formatDate(bookings[i].bookingDate)}
                           bookingTime={bookings[i].bookingTime}
                           bookingLength={bookings[i].bookingLength}
                           facility={bookings[i].facilitiesId}/>
            {:else}
              <!--booking creating component-->
              <p class="font-bold text-3xl pb-8 text-[#1A1A1A]">Calendar</p>
              <Calendar bind:selectedDate/>

              {#if selectedDate}
                <div class="grid"> 
                  <div class="justify-self-center pt-6 pb-4">
                    <Toggle bind:selection/>
                  </div>
                </div>

                {#if selection == 1}
                  <NewBooking selectedMonth={selectedMonth} selectedDay={selectedDay} bind:selectedDate/>
                {:else}     
                      {#await activityLoading()}
                        <p class="m-5">loading...</p>
                      {:then available_activities}
                        {#each available_activities as activity}
                          <ActivityCard class="my-3" heading={activity.activityType} 
                                                     location='Studio' 
                                                     startTime={activity.activityStartTime}
                                                     sessionLength="1"/>
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
