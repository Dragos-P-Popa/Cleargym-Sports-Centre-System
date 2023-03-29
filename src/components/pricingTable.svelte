<script>
        import { PUBLIC_FACILITIES_URL } from '$env/static/public'
let facilities;
let activities; 

     async function facilityLoading() {
    // fetch all facilities
		const res = await fetch(PUBLIC_FACILITIES_URL + 'facilities', {
			method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
		})

    
	  facilities = await res.json()
    return facilities
	}

    async function activityLoading() {
    // fetch all activites
		const res = await fetch(PUBLIC_FACILITIES_URL + 'activities', {
			method: 'GET',
      headers: {
        "Content-Type": "application/json",
      }
		})

    activities = await res.json()
    return activities
	}
</script>





    <table class="w-full border-borderColor border mt-4 table-auto border-spacing-6 border-collapse">
        <thead>
        <tr>
            <th class=" border-borderColor border p-2">
                Facility
            </th>
            <th class=" border-borderColor border p-2">
                Activity
            </th>
            <th class=" border-borderColor border p-2">
                1 hour
            </th>
        </tr>
        </thead>
        <tbody>
        
            {#await facilityLoading()}
            {:then facilities}
            {#each facilities as facility}

            <tr>
            <td class=" border-borderColor border p-4">{facility.facilityName}</td>
            
            <td class=" border-borderColor border p-4">
                {#await activityLoading()}
                {:then activities}
                {#each activities as activity}             
                <ul>
                    <li class="p-2">
                        {activity.activityType}
                        
                    </li>
                </ul>
                {/each}
                {/await}
            </td>
            <td class=" border-borderColor border p-4">

            </td>


            </tr>    
            {/each}
            {/await}
            

        

        </tbody>
    </table>






