export { matchers } from './matchers.js';

export const nodes = [() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18'),
	() => import('./nodes/19'),
	() => import('./nodes/20'),
	() => import('./nodes/21'),
	() => import('./nodes/22')];

export const server_loads = [];

export const dictionary = {
	"/": [12],
	"/auth": [13,[2]],
	"/bookings": [14,[3]],
	"/dashboard": [15,[4]],
	"/employees/amend": [16,[5]],
	"/employees/book": [17,[6]],
	"/employees/memberships": [18,[7]],
	"/management/activities": [19,[8]],
	"/management/analytics": [20,[9]],
	"/management/facilities": [21,[10]],
	"/management/staff": [22,[11]]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};

export { default as root } from '../root.svelte';