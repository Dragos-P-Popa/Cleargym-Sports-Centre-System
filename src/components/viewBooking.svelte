<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import CancelButton from "./cancelButton.svelte";
    import SecondaryButton from "./secondaryButton.svelte";
    import { PUBLIC_BOOKINGS_URL } from "$env/static/public";

    // variables to be defined by page
    export let bookingNumber: number;
    export let bookedOn: string;
    export let facility: string;
    export let activity: number;
    export let bookingDate: string;
    export let bookingTime: string;
    export let bookingLength: string;
    export let user: any;

    // This variable controls whether the user is able to edit their booking details
    let editMode = false;
    // This variable stores the status of the email confirmation
    let emailConfirmation;
    // These variables are to store details about an activity
    let activityDetails: any;
    let activityType: string;
    
    // This variable controls whether the confirmation message for booking cancellation
    // should be displayed. It is set to 'false' by default.
    let cancellation_confirm = false;

    // When a booking is edited and saved, this variable is set to 'true'
    let saveChanges = false;

    /**
     * Toggles the edit mode.
     * 
     * @returns {void}
     */
    function toggleEdit() {
        editMode = !editMode;
    }

    /**
     * Sets the 'saveChanges' variable to 'true' when the user confirms their changes.
     * 
     * @returns {void}
    */
    function confirmedChanges() {
        saveChanges = true;
        console.log(saveChanges);
    }

    /**
     * Formats the date to YYYY/MM/DD format.
     * 
     * @param {Date} date - The date to format.
     * @returns {string} - The formatted date.
     */
    function formatDate(date: number) {
        var d = new Date(date),
            month = "" + (d.getMonth() + 1),
            day = "" + d.getDate(),
            year = d.getFullYear();
        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;

        return [year, month, day].join("/");
    }

    /**
     * Deletes a booking by sending a request to the server
     * 
     * @param {number} id - The ID of the booking to delete.
     * @returns {Promise<void>} - A Promise that resolves when the booking is deleted or errors.
    */
    async function deleteBooking(id: number) {
        const res = await fetch(PUBLIC_BOOKINGS_URL + "bookings/" + id, {
            method: "DELETE",
            // enable credentials when they are implemented in the bookings API
            //credentials: 'include'
        });

        // If the code returned from the Bookings API was 200
        if (res.status == 200) {
            // Set the 'display_confirm' value to 'true'
            cancellation_confirm = true;

            // Make a POST request to the cancellation email endpoint
            const res2 = await fetch(
                PUBLIC_BOOKINGS_URL + `/emails/cancellation/`+user.email, {
                    method: 'POST',
                    headers: {
                    "Content-Type": "application/json",
                    }
            })
            // Verify that the confirmation email was sent
            emailConfirmation = await res2.json()

            if (emailConfirmation === "Sent") {
                console.log("User email: " + user.email)
                console.log("The message was sent")
            } else {
                console.log("The message was not sent")
            }
        }
    }

    /**
     * Edits a booking by sending a request to the server
     * 
     * @param {Event} e - The event that triggered this function.
     * @returns {Promise<void>} - A Promise that resolves when the booking is edited or errors.
    */
    async function amendBooking(e: Event) {
        // prevent the form from submitting prior to executing this logic
        e.preventDefault();

        // Convert the event's target to an HTML form element
        const form = e.target as HTMLFormElement;

        // fetch form fields
        const formData = new FormData(form);

        const data: any = {};
        // for each form field, create new key and assign the correct value inputted
        // by the user
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }

        let formattedDate = formatDate(data.date);
        const res = await fetch(
            PUBLIC_BOOKINGS_URL + "bookings/" + bookingNumber,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                // enable credentials when they are implemented in the bookings API
                //credentials: 'include',
                body: JSON.stringify({
                    bookingDate: formattedDate,
                    bookingTime: data.time,
                    bookingLength: data.length,
                }),
            }
        );

        // Reset the input fields
        form.reset();
    }

    /**
     * Retrieves the name of an activity from the Facilities API
     * 
     * @param {number} activityId - The ID of the activity to retrieve.
     * @returns {Promise<string>} - A Promise that resolves with the activity name.
    */
    async function findActivityName(activityId : number) {
    
        // Retrieve the information about an activity with this ID
        const res4 = await fetch(`http://cleargym.live:3003/activity/${activityId}`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
            }
        })
        
        // Store the data returned by the API in the 'activityDetails' variable
        activityDetails = await res4.json()
    
        // Assign the activity type to the 'activityType' variable
        activityType = activityDetails.activityType

        // Return the activity type
        return activityType
    }
</script>

<div
    class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-auto"
>
    <!-- Display the details of a selected booking -->
    <div class="grid grid-cols-2">
        <div>
            <p class="px-4 text-4xl text-left text-[#1A1A1A] font-semibold">
                Booking #{bookingNumber}
            </p>
            <p class="px-4 font-light text-md text-[#515151] text-left">
                Booking details
            </p>
        </div>
        <div class="justify-self-end">
            <SecondaryButton on:click>Close</SecondaryButton>
        </div>
    </div>

    <hr class="m-6 rounded bg-[#EDEDEF]" />

    <div class="flex justify-between space-x-4 px-4 text-[#1A1A1A] mt-8 mb-8">
        <div class="py-1">
            <p class="font-semibold">Booked on</p>
            <p>{bookedOn}</p>
        </div>
        <div class="py-1">
            <p class="font-semibold">Paid with</p>
            <p>Stripe</p>
        </div>
        <!-- Display the name of an activity 
             by passing its ID to the findActivityName() function-->
        {#await findActivityName(activity)}
            <p class="m-5">loading...</p>
        {:then activityType} 
            <div class="py-1">
                <p class="font-semibold">Activity</p>
                <p>{activityType}</p>
            </div>
        {/await}

        <div class="py-1">
            <p class="font-semibold">Booked venue</p>
            <p>{facility}</p>
        </div>
    </div>

    <!--if viewing details, fields should be disabled-->
    {#if editMode == false}
        <div class="py-2 flex space-x-6 px-4 text-[#1A1A1A]">
            <div class="py-2 flex-1">
                <label for="date">Date</label> <br />
                <input
                    class="border-borderColor border-[1px] rounded-md 
                           px-2 py-2 mt-1 shadow-sm min-w-full"
                    type="date"
                    id="date"
                    name="date"
                    value={bookingDate}
                    disabled
                />
            </div>
            <div class="py-2 flex-1">
                <label for="time">Time</label> <br />
                <input
                    class="border-borderColor border-[1px] rounded-md 
                           px-2 py-2 mt-1 shadow-sm min-w-full"
                    type="time"
                    id="time"
                    name="time"
                    value={bookingTime}
                    disabled
                />
            </div>
        </div>
        <div class="py-2 px-4 text-[#1A1A1A]">
            <label for="length">Session Length</label> <br />
            <select
                class="border-borderColor border-[1px] rounded-md 
                       px-2 py-2 mt-1 shadow-sm min-w-full"
                name="length"
                id="length"
                disabled
            >
                {#if bookingLength == "01:00"}
                    <option selected value="01:00">1 hour</option>
                    <option value="02:00">2 hours</option>
                    <option value="03:00">3 hours</option>
                {:else if bookingLength == "02:00"}
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

        <div class="flex justify-between  space-x-6 px-4">
            <!-- When this button is clicked outside of edit mode, 
                 call the deleteBooking() function -->
            <CancelButton
                on:click={() => deleteBooking(bookingNumber)}
                class="mt-12 w-4/5 place-self-center"
                >Cancel booking</CancelButton
            >
            <!-- When this button is clicked outside of edit mode, 
                 call the toggleEdit() function -->
            <MainButton
                on:click={() => toggleEdit()}
                class="mt-12 w-4/5 place-self-center">Amend booking</MainButton
            >
        </div>
    <!--if editing, fields should be enabled-->
    {:else if editMode == true}
        <form on:submit={amendBooking}>
            <div class="py-2 flex space-x-6 px-4 text-[#1A1A1A]">
                <div class="py-2 flex-1">
                    <label for="date">Date</label> <br />
                    <input
                        class="border-borderColor border-[1px] rounded-md 
                               px-2 py-2 mt-1 shadow-sm min-w-full"
                        type="date"
                        id="date"
                        name="date"
                        value={bookingDate}
                    />
                </div>
                <div class="py-2 flex-1">
                    <label for="time">Time</label> <br />
                    <input
                        class="border-borderColor border-[1px] rounded-md 
                               px-2 py-2 mt-1 shadow-sm min-w-full"
                        type="time"
                        id="time"
                        name="time"
                        value={bookingTime}
                    />
                </div>
            </div>
            <div class="py-2 px-4 text-[#1A1A1A]">
                <label for="length">Session Length</label> <br />
                <select
                    class="border-borderColor border-[1px] rounded-md 
                           px-2 py-2 mt-1 shadow-sm min-w-full"
                    name="length"
                    id="length"
                >
                    <option selected value="01:00">1 hour</option>
                    <option value="02:00">2 hours</option>
                    <option value="03:00">3 hours</option>
                </select>
            </div>

            <div class="flex justify-between  space-x-6 px-4">
                <!-- When this button is clicked in edit mode, 
                     call the toggleEdit() function -->
                <CancelButton
                    on:click={() => toggleEdit()}
                    class="mt-12 w-4/5 place-self-center"
                    >Cancel amend</CancelButton
                >
                <!-- When this button is clicked in edit mode, 
                     call the confirmedChanges() function -->
                <MainButton
                    type="submit"
                    class="mt-12 w-4/5 place-self-center"
                    on:click={() => confirmedChanges()}
                    >Confirm amend</MainButton
                >
            </div>
        </form>
    {/if}

    <!-- If the booking deletion request was successful, 
         display a confirmation message -->
    {#if cancellation_confirm == true}
        <p
            class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
            style="font-size: 20px; color: green;"
        >
            The booking was deleted successfully!
        </p>
        <!-- The list of bookings gets refreshed after each successful deletion -->
        <script>
            setTimeout(() => {
                location.reload();
            }, 1500);
        </script>
    {/if}

    {#if saveChanges == true}
        <p
            class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
            style="font-size: 20px; color: green;"
        >
            The booking was amended successfully!
        </p>
        <!-- The list of bookings gets refreshed after each successful amendment -->
        <script>
            setTimeout(() => {
                location.reload();
            }, 1500);
        </script>
    {/if}
</div>
