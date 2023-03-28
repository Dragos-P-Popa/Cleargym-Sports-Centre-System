<script lang="ts">
    import JoinUsButton from "./joinUsButton.svelte";
    import ClientCard from "./clientCard.svelte";
    import MainButton from "./mainButton.svelte";
    import BookingCard from "./bookingCard.svelte";
    import BookingInfo from "./viewBooking.svelte";
    let found = false;
    let amendbooking = false;
    let amendMembership = false;
    let fName = "Name";
    let lName = "Surname";
    let email = "Email";
    let nonCustomer = false;
    let i = -1;

    let userId: string;

    import {
        PUBLIC_AUTH_URL,
        PUBLIC_BOOKINGS_URL,
        PUBLIC_FACILITIES_URL,
    } from "$env/static/public";
    import MembershipCard from "./membershipCard.svelte";

    async function bookingSwitch() {
        amendbooking = true;
        amendMembership = false;

        const res2 = await fetch(
            PUBLIC_BOOKINGS_URL + "bookings/user/" + userId,
            {
                method: "GET",
            }
        );

        let bookingsData = await res2.json();
        let bookings = [...bookingsData];

        return bookings;
    }

    function membershipSwitch() {
        amendbooking = false;
        amendMembership = true;
    }

    function findClientCard() {
        found = false;
        nonCustomer = false;
    }

    function setViewFocus(id: number) {
        i = id;
    }

    function formatDate(date: number) {
        var d = new Date(date),
            month = "" + (d.getMonth() + 1),
            day = "" + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;

        return [year, month, day].join("-");
    }

    async function accessClientData(e: { target: HTMLFormElement }) {
        const formData = new FormData(e.target);
        let result = null;
        const data: any = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }
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
        if (userDetails.status == 200) {
            const userD = await userDetails.json();
            console.log(userD);
            userId = userD[0]._id;
            fName = userD[0].firstName;
            lName = userD[0].lastName;
            email = userD[0].email;
            found = true;
        } else if (userDetails.status == 404) {
            nonCustomer = true;
        }
        e.target.reset();
    }
</script>

<div>
    <form on:submit|preventDefault={accessClientData}>
        <div class="flex flew-row w-full">
            <div class="flex flex-col w-full">
                <label for="customerEmail">Customer Email</label>
                <input
                    class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-ful w-full mb-10"
                    type="text"
                    id="customerEmail"
                    name="customerEmail"
                    required
                />
            </div>
            <div class="w-1/5">
                <JoinUsButton
                    class="items-end m-5 w-3/4 mt-7 h-10"
                    on:click={findClientCard}
                    type="submit">Search</JoinUsButton
                >
            </div>
        </div>
    </form>
    {#if found}
        <div class="flex flex-row">
            <ClientCard
                class="w-5/6"
                heading="{fName}  {lName}"
                subheading={email}
            />
            <div class="flex flex-col">
                <MainButton class="m-8 w-5/6" on:click={bookingSwitch}
                    >Bookings</MainButton
                >
                <MainButton class="m-8 w-5/6" on:click={membershipSwitch}
                    >Membership</MainButton
                >
            </div>
        </div>
    {/if}

    {#if nonCustomer}
        <p class="text-sm text-[#e20f14]">non existing customer</p>
    {/if}

    {#if amendbooking}
        <div class="overflow-y-auto h-[80vh] mt-16 flex flex-row">
            <div class="flex flex-col w-1/2">
                <!--display all bookings-->
                {#await bookingSwitch()}
                    <p class="m-5">loading...</p>
                    <!--when response is recieved, load data into the html-->
                {:then bookings}
                    {#each bookings as b, i}
                        <BookingCard
                            on:click={() => setViewFocus(i)}
                            class="my-2 transition transform hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none"
                            heading="Booking #{b.id}"
                            subheading={b.bookingType}
                        />
                    {/each}

                    {#if i != -1}
                        <BookingInfo
                            on:click={() => (i = -1)}
                            bookingNumber={bookings[i].id}
                            bookedOn={bookings[i].createDate}
                            bookingDate={formatDate(bookings[i].bookingDate)}
                            bookingTime={bookings[i].bookingTime}
                            bookingLength={bookings[i].bookingLength}
                            facility={bookings[i].facilitiesId}
                        />
                    {/if}
                {/await}
            </div>
        </div>
    {/if}

    {#if amendMembership}
        <MembershipCard
            active="1"
            heading="No membership"
            subHeading="Pay as you go"
            bulletPoints={[
                "Most flexible option.",
                "Pay whenever you want to book.",
                "Perfect for newcomers who are looking to try out before committing to a membership.",
            ]}
            class="col-span-4"
        />
        <MembershipCard
            active="0"
            heading="Cleargym One"
            subHeading="All-inclusive membership"
            bulletPoints={[
                "Highest cost savings.",
                "Unlimited access to all of our facilities.",
                "One simple monthly payment.",
                "Cancel at any time.",
            ]}
            class="col-span-4"
        />
    {/if}

    <!-- if ammend booking -->
</div>
