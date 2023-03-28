<script>
    import JoinUsButton from "./joinUsButton.svelte";
    import ClientCard from "./clientCard.svelte";
    import MainButton from "./mainButton.svelte";

    let searchButton = false;
    let amendbooking = false;
    let amendMembership = false;

    import {
        PUBLIC_AUTH_URL,
        PUBLIC_BOOKINGS_URL,
        PUBLIC_FACILITIES_URL,
    } from "$env/static/public";
    import MembershipCard from "./membershipCard.svelte";

    function bookingSwitch() {
        amendbooking = true;
        amendMembership = false;
    }

    function membershipSwitch() {
        amendbooking = false;
        amendMembership = true;
    }

    function searchSwitch() {
        searchButton = true;
    }

    /*  async function accessClientData(e: { target: HTMLFormElement }) {
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
        const userD = await userDetails.json();
        let userId = userD[0]._id;
        let fName = userD[0].firstName;
        e.target.reset();
    } */
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
                />
            </div>
            <div class="w-1/5">
                <JoinUsButton
                    class="items-end m-5 w-3/4 mt-7 h-10"
                    on:click={searchSwitch}
                    type="submit">Search</JoinUsButton
                >
            </div>
        </div>
    </form>
    {#if searchButton}
        <div class="flex flex-row">
            <ClientCard class="w-5/6" heading="Name" subheading="email" />
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
