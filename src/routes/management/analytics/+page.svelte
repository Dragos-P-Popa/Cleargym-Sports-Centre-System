<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import { browser } from '$app/environment'; 
  import { onMount } from "svelte";
  import { PUBLIC_ANALYTICS_URL } from '$env/static/public'

  export let data;
  let user = data.user;
  let facilities = data.facilities;
  let sales = data.sales;

  function preProcessFacilityNames() {
    let facilityNames : any = [];

    facilities.forEach((facility : any) => {
      facilityNames.push(facility.facilityName)
    });

    return facilityNames;
  }

  function preProcessFacilitySales() {
    let facilitySales = new Array(facilities.length).fill(0);

    sales.forEach((sale : any) => {
      facilitySales[sale.facilityId] = facilitySales[sale.facilityId] + 1
    });

    return facilitySales
  }

  onMount(async () => {

  let facilityNames : any = await preProcessFacilityNames();
  let facilitySales : any = await preProcessFacilitySales();

  if (browser) {
    const barFacilities = document.getElementById('barFacilities');
    
    new Chart(barFacilities, {
      type: 'bar',
      data: {
        labels: facilityNames,
        datasets: [{
          label: 'Total sales per facility (sessions)',
          data: facilitySales,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    const lineFacilities = document.getElementById('lineFacilities');

    new Chart(lineFacilities, {
      type: 'line',
      data: {
        labels: ['Swimming pool', 'Fitness room', 'Climbing wall', 'Sports hall', 'Studio', 'Squash court'],
        datasets: [{
          label: '# of Visits per week',
          data: [12, 19, 3, 5, 12, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    const barActivities = document.getElementById('barActivities');

    new Chart(barActivities, {
      type: 'bar',
      data: {
        labels: ['Yoga', 'Pilates', 'Lane swimming', 'General use', '1-hour sessions', 'Aerobics'],
        datasets: [{
          label: '# of Visits per week',
          data: [12, 5, 7, 5, 13, 11],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    const lineActivities = document.getElementById('lineActivities');

    new Chart(lineActivities, {
      type: 'line',
      data: {
        labels: ['Swimming pool', 'Fitness room', 'Climbing wall', 'Sports hall', 'Studio', 'Squash court'],
        datasets: [{
          label: '# of Visits per week',
          data: [12, 5, 7, 5, 13, 11],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
})
</script>

<div class="grid grid-cols-12">
  <NavBar active=3 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Analytics</p>
        <p class="font-light text-2xl text-[#515151]">view sports centre statistics</p>
        <div class="w-full">
          <p class="pt-10 font-light text-2xl text-[#1A1A1A]">Facilities</p>
          <canvas id="barFacilities"></canvas>
         <!-- <canvas id="lineFacilities"></canvas> -->
        </div>
        <!-- <div>
          <p class="pt-10 font-light text-2xl text-[#1A1A1A]">Activities</p>
          <canvas id="barActivities"></canvas>
          <canvas id="lineActivities"></canvas>
        </div>-->
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>