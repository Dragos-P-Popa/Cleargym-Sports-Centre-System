<script lang="ts">
  import { onMount } from 'svelte';
  import { PUBLIC_BOOKINGS_URL, PUBLIC_PAYMENTS_URL } from '$env/static/public'

  export let data;

  let basketItems = data.basket.items;
  let user = data.user;

  let itemWorkingCopy = basketItems;

  function createBookings(){
    let item = itemWorkingCopy[0]

    console.log("before: " + itemWorkingCopy)

    let userId = localStorage.getItem("uid");
    let facilitiesId = item.facilityId;
    let bookingDate = item.bookingDate;
    let bookingTime = item.bookingTime;
    let bookingLength = item.bookingLength;
    let bookingType = item.bookingType;

    const res = fetch(PUBLIC_BOOKINGS_URL + 'booking', {
      method: 'POST',
      // essential to set the header
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userId,
        facilityId: facilitiesId,
        activityId: 1,
        bookingDate: "2023/03/31",
        bookingTime: "11:00",
        bookingLength
      })
    }).then((result) =>{
      if (result.status) {
        //if 200...
        itemWorkingCopy.shift();

        console.log("after: " + itemWorkingCopy)

        if (itemWorkingCopy.length > 0){
          setTimeout( createBookings, 500 );
        } else {
          const res = fetch(PUBLIC_PAYMENTS_URL + 'basket/'+user._id, {
            method: 'DELETE',
            // essential to set the header
            headers: {
              "Content-Type": "application/json",
            }
          })
        }
      }
    })
  }

  onMount(() => { 

    createBookings();

  });

</script>

<div class="p-16">

  <p>Dear {user.firstName} {user.lastName}, thank you for your order!</p>

</div>

<style lang="postcss">
 
</style>