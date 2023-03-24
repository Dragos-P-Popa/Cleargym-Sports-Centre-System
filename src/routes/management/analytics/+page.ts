import { PUBLIC_AUTH_URL, PUBLIC_BOOKINGS_URL } from '$env/static/public'

/*
    This file runs on page load. It makes some API calls and forwards 
    the data to the dashboard page
*/

export async function load({ fetch, request }) {
    
    const res = await fetch(PUBLIC_AUTH_URL + 'user/', {
			method: 'GET',
      credentials: 'include',
    })

    let user = await res.json();
  
    if (user) {
      return { user }
    }
}