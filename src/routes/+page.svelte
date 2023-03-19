<script>
  import SecondaryButton from "../components/secondaryButton.svelte";
  import Carousel from "../components/facilityCarousel.svelte";
  import Footer from "../components/footer.svelte";
  import Welcome from "../components/welcomeJoinUs.svelte";
  import Star from "../components/starFacilities.svelte";
  import Activities from "../components/activityInfo.svelte";
  import MembershipCard from "../components/membershipCard.svelte";
  import { goto } from "$app/navigation";
  import "@fontsource/manrope";
</script>

<div>
  <img class="place-self-left pt-4 pl-6" src="logo.svg" alt="logo" />
  <div class="absolute right-0 top-0 pt-4 pr-6">
    <SecondaryButton on:click={() => goto("/dashboard")}
      >Dashboard</SecondaryButton
    >
  </div>
  <div><Welcome /></div>
  <div><Star /></div>
  <div><Activities /></div>
  <div class="py-10 px-48 text-[#1A1A1A] text-[48px]">
    <p><b>Pricing & memberships</b></p>
  </div>
  <div class="px-48">
    <MembershipCard
      active="0"
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
  </div>
  <div><Carousel /></div>
  <div><Footer /></div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
