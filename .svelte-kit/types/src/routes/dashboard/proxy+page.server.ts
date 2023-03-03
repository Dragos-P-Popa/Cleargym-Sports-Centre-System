// @ts-nocheck
import { error } from '@sveltejs/kit'
import type { PageServerLoad } from './$types';


export const load = async () => {   
    const res = await fetch('http://localhost:3001/user/', {
			method: 'GET',
            credentials: 'include',
        })

        let userData = await res.json();
        let user = [...userData];
  
    if (user) {
      return { user }
    }
  
    error(404, 'Not found')
};null as any as PageServerLoad;