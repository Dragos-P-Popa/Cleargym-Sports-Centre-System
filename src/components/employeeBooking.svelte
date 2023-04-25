<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import {
        PUBLIC_AUTH_URL,
        PUBLIC_BOOKINGS_URL,
        PUBLIC_FACILITIES_URL,
    } from "$env/static/public";

    let facilities: any;
    let selectedFacility: number;
    export let selectedDate: Date;
    let nonCustomer = false;

    function nonCustomerMessage() {
        nonCustomer = false;
    }

    // This variable controls whether the confirmation message should be displayed.
    // It is set to 'false' by default.
    let display_confirm = false;

    function formatDate(date: number, char: string) {
        // converts date from DateTime to yr/mth/day
        var d = new Date(date),
            month = "" + (d.getMonth() + 1),
            day = "" + d.getDate(),
            year = d.getFullYear();

        // if day or month is 1-9 return it as 01-09 instead
        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;

        return [year, month, day].join(char);
    }

    async function createBooking(e: { target: HTMLFormElement }) {
        // fetch form fields
        const formData = new FormData(e.target);
        // initialise a variable for the API response
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

        let userId = userD[0]._id;
        let facilitiesId = facilities[selectedFacility].id;
        let bookingDate = formatDate(Date.parse(data.date), "/");
        let bookingTime = data.time;
        let bookingLength = data.length;
        let bookingType = "General";

        console.log(
            JSON.stringify({
                userId,
                facilityId: facilitiesId,
                activityId: 1,
                bookingDate,
                bookingTime,
                bookingLength,
                bookingType,
            })
        );

        //create a request to the Auth API (make sure it is running on your machine to test)
        const res = await fetch(PUBLIC_BOOKINGS_URL + "booking", {
            method: "POST",
            // essential to set the header
            headers: {
                "Content-Type": "application/json",
            },
            // add email and password
            body: JSON.stringify({
                userId,
                facilityId: facilitiesId,
                activityId: 1,
                bookingDate,
                bookingTime,
                bookingLength,
                bookingType,
            }),
        });

        // wait in the background for API response
        result = await res.json();
        const code = await res.status;
        console.log(res.status);
        if (res.status == 200) {
            display_confirm = true;
        }

        // Reset the input fields in case a user wishes to make another booking
        e.target.reset();
    }

    async function facilityLoading() {
        // fetch all facilities
        const res = await fetch(PUBLIC_FACILITIES_URL + "facilities", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        // this data is used to populate the facility selection UI element (line 97-112)
        facilities = await res.json();
        return facilities;
    }
</script>

<div
    class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor"
>
    <p class="text-4xl text-center text-[#1A1A1A]">New Booking</p>
    <p class="font-light text-md text-[#515151] text-center">Staff Booking</p>

    <hr class="m-6 mx-24 rounded bg-borderColor" />

    <div
        class="border-[1px] h-28 overflow-auto mb-4 select-none border-borderColor divide-borderColor rounded-lg shadow-sm divide-y"
    >
        <!--call facilityLoading and wait for API response. While waiting display "loading..."-->
        {#await facilityLoading()}
            <p class="m-5">loading...</p>
            <!--when response is recieved, load data into the html-->
        {:then facilities}
            <!--create new div for each facility-->
            {#each facilities as facility, i}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div
                    on:click={() => (selectedFacility = i)}
                    class="flex justify-between hover:bg-silver"
                >
                    <p class="p-2 h-10">{facility.facilityName}</p>
                    {#if selectedFacility == i}
                        <!--if a facility is selected by clicking on it, display a checkmark icon-->
                        <svg
                            class="self-center mr-2"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22Z"
                                stroke="#106EA2"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            />
                            <path
                                d="M7.75 12L10.58 14.83L16.25 9.17"
                                stroke="#106EA2"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            />
                        </svg>
                    {/if}
                </div>
            {/each}
        {/await}
    </div>

    <form on:submit|preventDefault={createBooking}>
        <div class="flex flex-row items-start">
            <div class="py-2 pr-3">
                <label for="date">Date</label> <br />
                <input
                    class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full"
                    type="date"
                    id="date"
                    name="date"
                    value={formatDate(selectedDate, "-")}
                />
            </div>
            <div class="py-2 px-2">
                <label for="time">Time</label> <br />
                <input
                    class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full"
                    type="time"
                    id="time"
                    name="time"
                    value=""
                />
            </div>
            <div class="py-2 px-3">
                <label for="length">Length</label> <br />
                <select
                    class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full"
                    name="length"
                    id="length"
                >
                    <option value="01:00">1 hour</option>
                    <option value="02:00">2 hours</option>
                </select>
            </div>
        </div>
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

    <!-- If the request was successful, display a confirmation message -->
    {#if display_confirm == true}
        <p
            class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
            style="font-size: 20px; color: green;"
        >
            The booking was completed successfully!
        </p>
        <!-- The list of bookings gets refreshed after each successful submission -->
        <script>
            setTimeout(() => {
                location.reload();
            }, 1500);
        </script>
    {/if}

    {#if nonCustomer == true}
        <p
            class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
            style="font-size: 20px; color: red;"
        >
            Not a customer email
        </p>
    {/if}
</div>
