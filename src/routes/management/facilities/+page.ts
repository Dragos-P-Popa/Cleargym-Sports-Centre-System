import { PUBLIC_AUTH_URL, PUBLIC_FACILITIES_URL } from '$env/static/public'

/*
    This file runs on page load. It makes some API calls and forwards 
    the data to the manager facilities page
*/

export async function load({ fetch, request }) {
    
    const res = await fetch(PUBLIC_AUTH_URL + 'user/', {
			method: 'GET',
      credentials: 'include',
    })

    let user = await res.json();

    const res2 = await fetch(PUBLIC_FACILITIES_URL + 'facilities', {
      method: 'GET',
    })

    let facilitiesData = await res2.json();
    let facilities = [...facilitiesData];
  
    if (user) {
      return { user, facilities }
    }
}