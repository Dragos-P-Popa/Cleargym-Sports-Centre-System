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
            {#if prices}
              {#each basket.items as basketItem, i}
                {basketItem.bookingType} - {basketItem.bookingDate} ...................... £{prices[i]}<br>
              {/each}
            {/if}
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