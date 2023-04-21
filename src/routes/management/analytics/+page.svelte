<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import { browser } from '$app/environment'; 
  import { onMount } from "svelte";
  import { PUBLIC_ANALYTICS_URL } from '$env/static/public'

  export let data;
  let user = data.user;
  // all facilities
  let facilities = data.facilities;
  // all activities
  let activities = data.activities;
  // all sales
  let sales = data.sales;

  // creates an array of facility names which can be used for the graph labels
  // ["swimming pool", "gym" ...]
  function preProcessFacilityNames() {
    let facilityNames : any = [];

    facilities.forEach((facility : any) => {
      facilityNames.push(facility.facilityName)
    });

    return facilityNames;
  }

  // creates an array of activity names which can be used for the graph labels
  // ["yoga", "pilates" ...]
  function preProcessActivityNames() {
    let activityType : any = [];

    activities.forEach((activity : any) => {
      activityType.push(activity.activityType)
    });

    return activityType;
  }

  // creates a list of total sessions sold per facility
  // index correlates with facility ID so index 0 in facilityUsage array is the total sales for facilityId 0
  function preProcessFacilityUsage() {
    let facilityUsage = new Array(facilities.length).fill(0);

    // loop over every sale and increment index which current sale relates to. E.g. when sale has facilityId 4, the 4th index in the facilitySales array gets incremented
    sales.forEach((sale : any) => {
      facilityUsage[sale.facilityId] = facilityUsage[sale.facilityId] + 1;
    });
    
    return facilityUsage
  }

  // creates a list of total sessions sold per facility
  // index correlates with facility ID so index 0 in facilitySales array is the total sales for facilityId 0
  function preProcessFacilitySales() {
    let facilitySales = new Array(facilities.length).fill(0);

    // loop over every sale and increment index which current sale relates to. E.g. when sale has facilityId 4, the 4th index in the facilitySales array gets incremented
    sales.forEach((sale : any) => {
      facilitySales[sale.facilityId] = sale.saleValue;
    });
    
    return facilitySales
  }

  // creates a list of total sessions sold per activity
  // index correlates with activity ID so index 0 in activitySales array is the total sales for activityId 0
  function preProcessActivityUsage() {
    let activityUsage = new Array(activities.length).fill(0);

    // loop over every sale and increment index which current sale relates to. E.g. when sale has activityId 4, the 4th index in the activitySales array gets incremented
    sales.forEach((sale : any) => {
      activityUsage[sale.activityId] = activityUsage[sale.activityId] + 1
    });

    return activityUsage
  }

  // creates a list of total sessions sold per facility
  // index correlates with facility ID so index 0 in facilitySales array is the total sales for facilityId 0
  function preProcessActivitySales() {
    let activitySales = new Array(activities.length).fill(0);

    // loop over every sale and increment index which current sale relates to. E.g. when sale has facilityId 4, the 4th index in the facilitySales array gets incremented
    sales.forEach((sale : any) => {
      activitySales[sale.activityId] = sale.saleValue;
    });
    
    return activitySales
  }

  onMount(async () => {

  // await so that code does not progress until values have been returned by the functions
  // avoid undefined values
  let facilityNames : any = await preProcessFacilityNames();
  let facilityUsage : any = await preProcessFacilityUsage();
  let facilitySales : any = await preProcessFacilitySales();
  let activityNames : any = await preProcessActivityNames();
  let activityUsage : any = await preProcessActivityUsage();
  let activitySales : any = await preProcessActivitySales();
  let date : any = sales.saleDate;

  const today = new Date();
  const weekStart = new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay());
  const weekEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate() + (6 - today.getDay()));
  const weekRange = weekStart.toLocaleDateString() + " - " + weekEnd.toLocaleDateString();

  // update graph title
  const graphTitle = `${weekRange}`;

  if (browser) {
    const barFacilities = document.getElementById('barFacilities');
    
    new Chart(barFacilities, {
      type: 'bar',
      data: {
        // set labels to all facilities
        labels: facilityNames,
        datasets: [{
          label: 'Total sales per facility (sessions)',
          // sales data
          data: facilitySales,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              // include a gbp sign in the ticks
              callback: function(value) {
                  return '£' + value;
              }
            }
          }
        },
        plugins: {
            // title of the graph
            title: {
                display: true,
                text: 'Sales for ' + graphTitle
            },
            // put legend on the bottom
            legend: {
              display: true,
              position: 'bottom'
            }
        }
      }
    });
    const lineFacilities = document.getElementById('lineFacilities');

    new Chart(lineFacilities, {
      type: 'line',
      data: {
        // set labels to all facilities
        labels: facilityNames,
        datasets: [{
          label: 'Total usage per facility (sessions)',
          // usage data
          data: facilityUsage,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
            // title of the graph
            title: {
                display: true,
                text: 'Usage for ' + graphTitle
            },
            // put legend on the bottom
            legend: {
              display: true,
              position: 'bottom'
            }
        }
      }
    });
    const barActivities = document.getElementById('barActivities');

    new Chart(barActivities, {
      type: 'bar',
      data: {
        // set labels to all activities
        labels: activityNames,
        datasets: [{
          label: 'Total sales per activity (sessions)',
          // sales data
          data: activitySales,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              // include a gbp sign in the ticks
              callback: function(value) {
                  return '£' + value;
              }
            }
          }
        },
        plugins: {
            // title of the graph
            title: {
                display: true,
                text: 'Sales for ' + graphTitle
            },
            // put legend on the bottom
            legend: {
              display: true,
              position: 'bottom'
            }
        }
      }
    });
    const lineActivities = document.getElementById('lineActivities');

    new Chart(lineActivities, {
      type: 'line',
      data: {
        // set labels to all activities
        labels: activityNames,
        datasets: [{
          label: 'Total sales per activity (sessions)',
          // sales data
          data: activityUsage,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
            // title of the graph
            title: {
                display: true,
                text: 'Usage for ' + graphTitle
            },
            // put legend on the bottom
            legend: {
              display: true,
              position: 'bottom'
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
      <div class="col-span-7">
        <p class="font-bold text-5xl text-[#1A1A1A]">Analytics</p>
        <p class="font-light text-2xl text-[#515151]">view sports centre statistics</p>
        <div class="grid w-full">
          <p class="pt-10 font-light text-2xl text-[#1A1A1A]">Facilities</p>
          <canvas id="barFacilities"></canvas><br><br>
          <canvas id="lineFacilities"></canvas>
        </div>
        <div class="w-full">
          <p class="pt-10 font-light text-2xl text-[#1A1A1A]">Activities</p>
          <canvas id="barActivities"></canvas><br><br>
          <canvas id="lineActivities"></canvas><br>
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>