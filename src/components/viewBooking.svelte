<script>
    import MainButton from "./mainButton.svelte"
    import CancelButton from "./cancelButton.svelte"
</script>

<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="px-4 text-4xl text-left text-[#1A1A1A] font-semibold">Booking #1324</p>
    <p class="px-4 font-light text-md text-[#515151] text-left">Booking details</p>

    <hr class="m-6 rounded bg-[#EDEDEF]">

    <div class="flex justify-between space-x-4 px-4 text-[#1A1A1A]">
        <div class="py-1">
            <p class="font-semibold">Booked on</p>
            <p>27/02/2023</p>
        </div>
        <div class="py-1">
            <p class="font-semibold">Paid with</p>
            <p>Paypal</p>
        </div>
        <div class="py-1">
            <p class="font-semibold">Booked venue</p>
            <p>Swimming pool</p>
        </div>
    </div>
    

    <form>
        <div class="py-2 flex space-x-6 px-4 text-[#1A1A1A]">
            <div class="py-2 flex-1">
                <label for="date">Date</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="date" id="date" name="date" value="" disabled/>
            </div>
            <div class="py-2 flex-1">
                <label for="time">Time</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value=""disabled/>
            </div>
        </div>
        <div class="py-2 px-4 text-[#1A1A1A]">
          <label for="length">Session Length</label> <br>
          <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length" disabled>
            <option value="one">1 hour</option>
            <option value="two">2 hours</option>
          </select>
        </div>
    
        <div class="flex justify-between  space-x-6 px-4">
            <CancelButton type="submit" class="mt-12  w-4/5 place-self-center">Cancel booking</CancelButton>
            <MainButton type="submit" class="mt-12  w-4/5 place-self-center">Amend booking</MainButton>
        </div>
      </form>
</div>