<script>
  import SecondaryButton from "../components/secondaryButton.svelte";
  import Carousel from "../components/facilityCarousel.svelte";
  import Footer from "../components/footer.svelte";
  import Welcome from "../components/welcomeJoinUs.svelte";
  import Star from "../components/starFacilities.svelte";
  import Activities from "../components/activityInfo.svelte";
  import { goto } from "$app/navigation";
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
  <div><Carousel /></div>
  <div><Footer /></div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "Manrope";
  }
</style>
