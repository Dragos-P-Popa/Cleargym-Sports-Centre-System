
export async function load({ fetch, request }) {
    
    const res = await fetch('http://localhost:3001/user/', {
			method: 'GET',
      credentials: 'include',
    })

    let user = await res.json();

    const res2 = await fetch('http://127.0.0.1:3002/bookings/user/'+user._id, {
        method: 'GET'
    })

    let bookingsData = await res2.json();
    let bookings = [...bookingsData];
  
    if (user) {
      return { user, bookings }
    }
  }