<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../components/navbar.svelte"
  import MainButton from "../../components/mainButton.svelte"
  import { PUBLIC_PAYMENTS_URL, PUBLIC_FACILITIES_URL } from '$env/static/public'
  import { onMount } from "svelte";

  export let data;

  let basket = data.basket;
  let user = data.user;
  let checkoutUrl = PUBLIC_PAYMENTS_URL + "checkout/"+user._id
  let prices : any = basket.prices;
  let facilities: any[] = [];
  let activities: any[] = [];
  let facilityName: string;
  let activityName: string;


  async function dataLoading() {
    // fetch all facilities
    const res1 = await fetch(`http://cleargym.live:3003/facilities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // this data is used to populate the 'facilities' array
    facilities = await res1.json()

    // fetch all activities
    const res2 = await fetch(`http://cleargym.live:3003/activities`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
    })
    // this data is used to populate the 'activities' array
    activities = await res2.json()
  }


  function findFacilityName(facilityId : number) {
    // Iterate over the array of facilities
    for (let i = 0; i < facilities.length; i++) {
      // If a given 'facilityId' is found, return the facility's name
      if (facilities[i].id == facilityId) {
        return facilities[i].facilityName
      }
    }
  }


  function findActivityName(activityId : number) {
    // Iterate over the array of activities
    for (let i = 0; i < activities.length; i++) {
      // If a given 'activityId' is found, return the activity's name
      if (activities[i].activityId == activityId) {
        return activities[i].activityType
      }
    }
  }

  /* Load the required data into the 'activities' and 'facilities' arrays
     when the page is loaded */
  onMount(() => {
    dataLoading();
  });

</script>

<div class="grid grid-cols-12">
  <NavBar active=2 firstName={user.firstName} lastName={user.lastName}/>
  <div class="col-span-10 pt-12 px-8">
    <div class="">
      <p class="font-bold text-5xl text-[#1A1A1A]">Your basket...</p>
      <p class="font-light text-2xl ml-2 text-[#515151]">view and manage your basket</p> 
      {#if basket.items}
        <div class="rounded-md border-[1px] border-borderColor w-3/5 mt-16 p-5">
          <p class="font-bold text-3xl text-[#1A1A1A] mb-6">Your items</p>
          <p class="">
          {#await dataLoading()}
            <p>loading...</p>
          {:then}
          {#if prices}
            {#each basket.items as basketItem, i}
              {findFacilityName(basketItem.facilityId)} - {findActivityName(basketItem.activityId)} - {basketItem.bookingDate} ...................... £{prices[i]}<br>
            {/each}
          {/if}
          {/await}
          </p>      
        <form action="{checkoutUrl}" method="POST">
          <MainButton type="submit" class="mt-12 w-2/5 place-self-center">Checkout</MainButton>
        </form>
      </div>
      {:else}
        <p class="font-bold text-2xl text-[#1A1A1A] m-8">Your basket is empty</p>
      {/if}
    </div>
  </div>
</div>

<style lang="postcss">
 
</style>