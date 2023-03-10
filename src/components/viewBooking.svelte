<script lang="ts">
    import MainButton from "./mainButton.svelte"
    import CancelButton from "./cancelButton.svelte"

    export let bookingNumber : number;
    export let bookedOn : string;
    export let facility : number;
    export let bookingDate : string;
    export let bookingTime : string;
    export let bookingLength : string;

    async function deleteBooking(id : number){
        const res = await fetch('http://localhost:3002/bookings/'+id, {
			method: 'DELETE'
            // enable credentials when they are implemented in the bookings API
            //credentials: include
        })
    }
</script>

<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-8">
    <p class="px-4 text-4xl text-left text-[#1A1A1A] font-semibold">Booking #{bookingNumber}</p>
    <p class="px-4 font-light text-md text-[#515151] text-left">Booking details</p>

    <hr class="m-6 rounded bg-[#EDEDEF]">

    <div class="flex justify-between space-x-4 px-4 text-[#1A1A1A] mt-8 mb-8">
        <div class="py-1">
            <p class="font-semibold">Booked on</p>
            <p>{bookedOn}</p>
        </div>
        <div class="py-1">
            <p class="font-semibold">Paid with</p>
            <p>Paypal</p>
        </div>
        <div class="py-1">
            <p class="font-semibold">Booked venue</p>
            <p>{facility}</p>
        </div>
    </div>
    

    <form>
        <div class="py-2 flex space-x-6 px-4 text-[#1A1A1A]">
            <div class="py-2 flex-1">
                <label for="date">Date</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="date" id="date" name="date" value="{bookingDate}" disabled/>
            </div>
            <div class="py-2 flex-1">
                <label for="time">Time</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="{bookingTime}" disabled/>
            </div>
        </div>
        <div class="py-2 px-4 text-[#1A1A1A]">
          <label for="length">Session Length</label> <br>
          <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length" disabled>
            {#if bookingLength=="01:00"}
            <option selected value="one">1 hour</option>
            <option value="two">2 hours</option>
            <option value="three">3 hours</option>
            {:else if bookingLength=="02:00"}
            <option value="one">1 hour</option>
            <option selected value="two">2 hours</option>
            <option value="three">3 hours</option>
            {:else}
            <option value="one">1 hour</option>
            <option value="two">2 hours</option>
            <option selected value="three">3 hours</option>
            {/if}
          </select>
        </div>
    
        <div class="flex justify-between  space-x-6 px-4 pt-16">
            <CancelButton on:click={() => deleteBooking(bookingNumber)} class="mt-12 w-4/5 place-self-center">Cancel booking</CancelButton>            
            <MainButton class="mt-12 w-4/5 place-self-center">Amend booking</MainButton>
        </div>
      </form>
</div>