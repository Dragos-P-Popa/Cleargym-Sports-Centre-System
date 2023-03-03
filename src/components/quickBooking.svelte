<script>
    import MainButton from "./mainButton.svelte"
</script>

<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Quick booking</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new booking at one of our facilities.</p>

    <hr class="m-6 mx-24 rounded bg-borderColor">


    <div class="border-[1px] mb-4 select-none border-borderColor divide-borderColor rounded-lg shadow-sm divide-y">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <p class="p-2 hover:bg-silver ">Swimming pool</p> 
        <p class="p-2 hover:bg-silver ">Gym</p>
        <p class="p-2 hover:bg-silver ">Climbing wall</p>
    </div>

    <form>
        <div class="py-2">
          <label for="time">Time</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="" />
        </div>
        <div class="py-2">
          <label for="date">Date</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="date" id="date" name="date" value="" />
        </div>
        <div class="py-2">
          <label for="length">Length</label> <br>
          <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
            <option value="one">1 hour</option>
            <option value="two">2 hours</option>
          </select>
        </div>
    
        <div class="grid">
          <MainButton type="submit" class="mt-12  w-4/5 place-self-center">Checkout</MainButton>
        </div>
      </form>
</div>