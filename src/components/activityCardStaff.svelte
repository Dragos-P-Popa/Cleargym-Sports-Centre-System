<script lang="ts">
    import {
        PUBLIC_AUTH_URL,
        PUBLIC_BOOKINGS_URL,
        PUBLIC_FACILITIES_URL,
    } from "$env/static/public";
    import MainButton from "./mainButton.svelte";

    // This variable is used to store the values of the form fields.
    let divProps = {
        class:
            [$$restProps.class] +
            "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none",
    };

    // These variables are used to store the values of the form fields.
    export let facilityId: number;
    export let activityId: number;
    export let heading: string;
    export let location: string;
    export let bookingDate: Date;
    export let bookingTime: string;
    export let bookingLength: string;

    let userId: string;

    // set the variable book to false by default - controls the pop up for email request
    let book = false;

    // It is set to 'false' by default.
    let display_confirm = false;

    let nonCustomer = false;

    /**
     * Formats the date to YYYY/MM/DD format.
     *
     * @param {Date} date - The date to format.
     * @returns {string} - The formatted date.
     */
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

    /**
     * Creates a new booking by sending a request to the server
     * with the user's booking information.
     *
     * @returns {Promise<void>} - A Promise that resolves when the booking is created or errors.
     */
    async function createBooking(e: { target: HTMLFormElement }) {
        // fetch form fields
        const formData = new FormData(e.target);

        let result = null;

        const data: any = {};
        // for each form field, create new key and assign the correct value inputted
        // by the user
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }

        console.log(data);

        const userDetails = await fetch(
            PUBLIC_AUTH_URL + "users/email/" + data.customerEmail,
            {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        console.log(userDetails.status);
        if (userDetails.status == 403 || userDetails.status == 404) {
            nonCustomer = true;
        }

        const userD = await userDetails.json();

        console.log(userD);

        userId = userD[0]._id;

        //create a request to the Auth API (make sure it is running on your machine to test)
        const res = await fetch(PUBLIC_BOOKINGS_URL + "booking", {
            method: "POST",
            // essential to set the header
            headers: {
                "Content-Type": "application/json",
            },
            // convert the data to JSON
            body: JSON.stringify({
                userId,
                facilityId,
                activityId,
                bookingDate: formatDate(new Date(bookingDate)),
                bookingTime,
                bookingLength,
            }),
        });

        // Wait in the background for API response
        result = await res.json();
        const code = await res.status;

        // If the code returned from the Bookings API was 200
        if (res.status == 200) {
            // Set the 'display_confirm' value to 'true'
            display_confirm = true;
        }
    }

    function bookToggle() {
        book = true;
    }

    function nonCustomerMessage() {
        nonCustomer = false;
    }
</script>

<!-- The 'divProps' variable is used to store the values of the form fields. -->
<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{heading}</p>
        <div class="flex grid grid-cols-2">
            <div>
                <p class="text-sm">{location}</p>
                <p class="text-sm">
                    Starts at {bookingTime} for {bookingLength} hour(s)
                </p>
            </div>
            <div class="justify-self-end">
                <MainButton on:click={bookToggle} class="py-1 px-2">
                    Add client
                </MainButton>
            </div>
        </div>

        {#if book == true}
            <form on:submit|preventDefault={createBooking}>
                <div class="py-2">
                    <label for="customerEmail">Customer Email</label> <br />
                    <input
                        class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full"
                        type="text"
                        id="customerEmail"
                        name="customerEmail"
                        required
                    />
                </div>
                <div class="grid">
                    <MainButton
                        type="submit"
                        class="mt-12 w-4/5 place-self-center"
                        on:click={nonCustomerMessage}>Book</MainButton
                    >
                </div>
            </form>
        {/if}

        {#if nonCustomer == true}
            <p
                class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
                style="font-size: 20px; color: red;"
            >
                Not a customer email
            </p>
        {/if}

        <!-- If the request was successful, display a confirmation message -->
        {#if display_confirm == true}
            <p
                class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
                style="font-size: 20px; color: green;"
            >
                The booking was successfully added to the basket!
            </p>
        {/if}
    </div>
</div>
