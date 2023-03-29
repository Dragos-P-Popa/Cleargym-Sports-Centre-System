import { PUBLIC_AUTH_URL, PUBLIC_PAYMENTS_URL } from '$env/static/public'

export async function load({ fetch, request }) {
  
  const res = await fetch(PUBLIC_AUTH_URL + 'user/', {
    method: 'GET',
          credentials: 'include',
      })

  let user = await res.json();

  const res2 = await fetch(PUBLIC_PAYMENTS_URL + 'basket/'+user._id, {
      method: 'GET'
    })

  let basket = await res2.json();

  if (user) {
    return { user, basket }
  }
}