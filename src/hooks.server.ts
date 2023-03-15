import { sequence } from '@sveltejs/kit/hooks';
import { redirect, type Handle } from '@sveltejs/kit';

/*
    This is svelte server side code that runs every time a fetch() 
    request is made somewhere in the code. This function is here to refresh
    the access token before completing the inital fetch request. This ensures that
    there is no Unauthorised response from the server while the users refresh token
    is valid
*/

const refreshToken = (async ({ event, resolve }) => {
    if (event.cookies.get('refreshToken')){
        // make sure token is refreshed
        const refreshRes = await fetch('http://localhost:3001/refresh/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                cookie: event?.request.headers.get('cookie'), // only relevant server-side
                credentials: 'include', // only relevant client-side
            },
            body: JSON.stringify({
                "audience": event.cookies.get('audience')
            })
        });

        // remove unecessary characters from cookie recieved in refreshRes
        var re = new RegExp("accessToken" + "=([^;]+)");
        let token = re.exec(refreshRes.headers.get('set-cookie'))
        token = token[0].slice(14, -2)

        // set the cleaned token to the current event
        event.cookies.set('accessToken', token)
    } 
    return await resolve(event);
}) satisfies Handle;

const routeProtection = (async ({ event, resolve }) => {
    if (event.url.pathname == "/auth" || event.url.pathname == "/") {
        // unprotected route
        return await resolve(event);
    } else {
        // protected route
        if (event.cookies.get('refreshToken') == "" || !event.cookies.get('refreshToken')){
            
            // refresh was unsuccessful
            // reset cookies
            event.cookies.set('accessToken', "")
            event.cookies.set('audience', "")
            // then redirect to auth page
            if (event.url.pathname != "/auth") {
                throw redirect(307, '/auth')
            }
        }
    }
    return await resolve(event);
}) satisfies Handle;
 
const runFetch = (async ({ event, resolve }) => {
    // run the event which triggered this hook
    const result = await resolve(event)
    return result
}) satisfies Handle;
 
export const handle = sequence(refreshToken, routeProtection, runFetch);
