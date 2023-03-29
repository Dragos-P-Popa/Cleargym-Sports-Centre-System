import { PUBLIC_AUTH_URL, PUBLIC_PAYMENTS_URL } from '$env/static/public'

export async function load({ fetch, request }) {

    const res = await fetch(PUBLIC_AUTH_URL + 'user/', {
			method: 'GET',
            credentials: 'include',
        })

    let user = await res.json();
    let basket;

    try {
      const res2 = await fetch(PUBLIC_PAYMENTS_URL + 'basket/'+user._id, {
        method: 'GET'
      })
  
      basket = await res2.json();
    } catch (error) {
      console.error(error)
      basket = {}
    }


      if (user) {
        return { user, basket }
      }
}