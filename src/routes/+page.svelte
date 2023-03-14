<script>
  import  MainButton from "../components/mainButton.svelte"
  import  SecondaryButton from "../components/secondaryButton.svelte"
  import  Carousel from "../components/facilityCarousel.svelte"
  import Footer from "../components/footer.svelte"
</script>

<div>
  <img class="place-self-left pt-4 pl-6" src = "logo.svg" alt="logo"/>
  <div class="absolute right-0 top-0 pt-4 pr-6"><SecondaryButton>Dashboard</SecondaryButton></div>
  <!-- <div><Carousel></Carousel></div> -->
  <div><Footer></Footer></div>
</div>

<style lang="postcss">
  :global(body) {
      font-family:"Manrope",
  }
</style>