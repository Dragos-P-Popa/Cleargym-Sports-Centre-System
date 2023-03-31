import { PUBLIC_AUTH_URL} from '$env/static/public'

/*
    This file runs on page load. It makes some API calls and forwards 
    the data to the employee page
*/

export async function load({ fetch, request }) {
    
    const res = await fetch(PUBLIC_AUTH_URL + 'user/', {
			method: 'GET',
      credentials: 'include',
    })

    let user = await res.json();

    const res2 = await fetch(PUBLIC_AUTH_URL + 'users/', {
      method: 'GET',
      credentials: 'include',
    })

    let usersData = await res2.json();
    let employees = [...usersData];
  
  
    if (user) {
      return { user, employees }
    }
}