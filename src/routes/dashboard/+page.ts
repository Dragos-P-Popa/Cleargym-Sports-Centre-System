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


    const res2 = await fetch(PUBLIC_BOOKINGS_URL + 'bookings/user/'+user._id, {
      method: 'GET'
    })

    let bookingsData = await res2.json();
    let bookings = [...bookingsData];
  
    if (user) {
      return { user, bookings }
    }
  }