<script>
    import "@fontsource/manrope";
    import BookingCard from "../../components/bookingCard.svelte";
    import QuickBooking from "../../components/quickBooking.svelte";
    import NavBar from "../../components/navbar.svelte";
    import MembershipCard from "../../components/membershipCard.svelte";
    import PricingTable from "../../components/pricingTable.svelte";
    import SecondaryButton from "../../components/secondaryButton.svelte";
    import Carousel from "../../components/homeCarousel.svelte";
    import { onMount, onDestroy } from "svelte";
    /** @type {import('./$types').PageData} */
    export let data;

    // data fetched from server-side-rendering (SSR)
    // +page.server.ts
    let user = data.user;
    let bookings = data.bookings;

    // window is undefined when this code is running on the server side.
    // svelte does some processing on the server side, see svelte docs for more info
    if (typeof window !== "undefined") {
        // if its running on client side, save the user id as a local variable
        localStorage.setItem("uid", user._id);
    }
</script>

<div class="grid grid-cols-12">
    <NavBar firstName={user.firstName} lastName={user.lastName} />

    <div class="col-span-10 pt-12 px-8">
        <div class="grid grid-cols-6">
            <div class="col-span-4">
                <p class="font-bold text-5xl text-[#1A1A1A]">
                    {user.firstName},
                </p>
                <!--<p>{u._id}</p>-->
                <p class="font-light text-2xl text-[#515151]">welcome back!</p>
                <Carousel />
                <div class="flex grid grid-cols-2 mt-2">
                    <h1 class="text-4xl mt-4">Memberships</h1>
                    <SecondaryButton class="p-4 ml-28 justify-self-end"
                        >Manage membership</SecondaryButton
                    >
                </div>
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
                <h1 class="text-4xl mt-12">Pricing</h1>
                <PricingTable />
            </div>
            <div class="col-span-2 px-4">
                <!--if the user has at least 1 booking, show one here-->
                {#if bookings?.length > 0}
                    <p class="text-4xl text-[#1A1A1A] pb-4">Next booking</p>
                    <BookingCard
                        class=""
                        heading={bookings[0].bookingType}
                        subheading={bookings[0].bookingTime}
                    />
                {/if}
                <!--booking creating component-->
                <QuickBooking />
            </div>
        </div>
    </div>
</div>

<style lang="postcss">
    :global(body) {
        font-family: "Manrope";
    }
</style>
