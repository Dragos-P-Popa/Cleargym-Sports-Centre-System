<script lang="ts">
    
    import { PUBLIC_PAYMENTS_URL } from "$env/static/public";
    import MainButton from "./mainButton.svelte"

    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let userId:string;
    export let facilityId:number;
    export let activityId:number;
    export let heading:string;
    export let location:string;
    export let bookingDate:Date;
    export let bookingTime:string;
    export let bookingLength:string;

    
    // This variable controls whether the confirmation message should be displayed.
    // It is set to 'false' by default.
    let display_confirm = false

    function formatDate(date: Date) {
        
        var month = "" + (date.getMonth() + 1),
            day = "" + date.getDate(),
            year = date.getFullYear();

        if (month.length < 2) {
            month = "0" + month;
        } 
        if (day.length < 2) {
            day = "0" + day;
        }

        return [year, month, day].join("/");
        }


    async function createBooking() {

        // initialise a variable for the API response
        let result = null
        
        console.log(userId)

        //create a request to the Auth API (make sure it is running on your machine to test)
        const res = await fetch(PUBLIC_PAYMENTS_URL + `basket/`+userId, {
            method: 'POST',
            // essential to set the header
            headers: {
            "Content-Type": "application/json",
            },
            // add email and password
            body: JSON.stringify({
                userId,
                facilityId,
                activityId,
                bookingDate: formatDate(new Date(bookingDate)),
                bookingTime,
                bookingLength
            })
        })

        // wait in the background for API response
        result = await res.json()
        const code = await res.status

        // If the code returned from the Bookings API was 200
        if (res.status == 200)
        {
            // Set the 'display_confirm' value to 'true'
            display_confirm = true;
        }
    }

</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{heading}</p>
        <div class="flex grid grid-cols-2">
            <div>
                <p class="text-sm">{location}</p>
                <p class="text-sm">Starts at {bookingTime} for {bookingLength} hour(s)</p>
            </div>
            <div class="justify-self-end">
                <MainButton on:click={createBooking} 
                            class="py-1 px-2">
                            Checkout
                </MainButton>
            </div>
        </div>

        <!-- If the request was successful, display a confirmation message -->
        {#if display_confirm==true}
        <p class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
            style="font-size: 20px; color: green;">
            The booking was successfully added to the basket!
        </p>
        {/if}
    </div>
</div>