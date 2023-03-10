<script lang="ts">
    import MainButton from "./mainButton.svelte"
    import CancelButton from "./cancelButton.svelte"

    export let bookingNumber : number;
    export let bookedOn : string;
    export let facility : number;
    export let bookingDate : string;
    export let bookingTime : string;
    export let bookingLength : string;

    let editMode = false;

    function toggleEdit() {
        editMode = !editMode;
    }


  function formatDate(date : number) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2) 
          month = '0' + month;
      if (day.length < 2) 
          day = '0' + day;

      return [year, month, day].join('/');
    }

    async function deleteBooking(id : number){
        const res = await fetch('http://localhost:3002/bookings/'+id, {
			method: 'DELETE'
            // enable credentials when they are implemented in the bookings API
            //credentials: 'include'
        })
    }

    async function amendBooking(e: { target: HTMLFormElement; }){

        // fetch form fields
        const formData = new FormData(e.target);

        const data : any = {};
        // for each form field, create new key and assign the correct value inputted
        // by the user
        for (let field of formData) {
        const [key, value] = field;
        data[key] = value;
        }

        console.log(data);

        let formattedDate = formatDate(data.date);
        const res = await fetch('http://localhost:3002/bookings/'+bookingNumber, {
			method: 'PATCH',
            headers: {
                "Content-Type": "application/json",
            },
            // enable credentials when they are implemented in the bookings API
            //credentials: 'include',
			body: JSON.stringify({
				bookingDate: formattedDate,
                bookingTime: data.time,
                bookingLength: data.length
			})
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
    

    {#if editMode == false}
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
            <option selected value="01:00">1 hour</option>
            <option value="02:00">2 hours</option>
            <option value="03:00">3 hours</option>
            {:else if bookingLength=="02:00"}
            <option value="01:00">1 hour</option>
            <option selected value="02:00">2 hours</option>
            <option value="03::">3 hours</option>
            {:else}
            <option value="01:00">1 hour</option>
            <option value="02:00">2 hours</option>
            <option selected value="03:00">3 hours</option>
            {/if}
          </select>
        </div>

        <div class="flex justify-between  space-x-6 px-4 pt-16">
            <CancelButton on:click={() => deleteBooking(bookingNumber)} class="mt-12 w-4/5 place-self-center">Cancel booking</CancelButton>            
            <MainButton on:click={() => toggleEdit()} class="mt-12 w-4/5 place-self-center">Amend booking</MainButton>
        </div>
    {:else if editMode == true}
        <form on:submit|preventDefault={amendBooking}>
            <div class="py-2 flex space-x-6 px-4 text-[#1A1A1A]">
                <div class="py-2 flex-1">
                    <label for="date">Date</label> <br>
                    <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="date" id="date" name="date" value="{bookingDate}"/>
                </div>
                <div class="py-2 flex-1">
                    <label for="time">Time</label> <br>
                    <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="{bookingTime}"/>
                </div>
            </div>
            <div class="py-2 px-4 text-[#1A1A1A]">
              <label for="length">Session Length</label> <br>
              <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
                <option selected value="01:00">1 hour</option>
                <option value="02:00">2 hours</option>
                <option value="03:00">3 hours</option>
              </select>
            </div>

        <div class="flex justify-between  space-x-6 px-4 pt-16">
            <CancelButton on:click={() => toggleEdit()} class="mt-12 w-4/5 place-self-center">Cancel amend</CancelButton>            
            <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Confirm amend</MainButton>
        </div>  
        
    </form>
    {/if}

</div>