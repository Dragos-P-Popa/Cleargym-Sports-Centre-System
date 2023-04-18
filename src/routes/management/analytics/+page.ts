import { PUBLIC_AUTH_URL, PUBLIC_FACILITIES_URL, PUBLIC_ANALYTICS_URL } from '$env/static/public'

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

  const res2 = await fetch(PUBLIC_FACILITIES_URL + 'facilities', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
    }
  })

  let facilities = await res2.json()

  const res3 = await fetch(PUBLIC_ANALYTICS_URL + 'sales', {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
    }
  })

  let sales = await res3.json()

  if (user) {
    return { user, facilities, sales }
  }
}