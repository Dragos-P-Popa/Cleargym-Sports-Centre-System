import { sequence } from "@sveltejs/kit/hooks";

export async function handle({ event, resolve }) {
    
    const result = await resolve(event);
    console.log(result.status)
    // TO-DO :: Global handle 401. 
    // if the response is ever 401, try to refresh token then retry request with new token
    return result;
  }