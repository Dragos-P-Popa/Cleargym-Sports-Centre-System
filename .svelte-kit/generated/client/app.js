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
	() => import('./nodes/20')];

export const server_loads = [];

export const dictionary = {
	"/": [11],
	"/auth": [12,[2]],
	"/bookings": [13,[3]],
	"/dashboard": [14,[4]],
	"/employees/amend": [15,[5]],
	"/employees/book": [16,[6]],
	"/management/activities": [17,[7]],
	"/management/analytics": [18,[8]],
	"/management/facilities": [19,[9]],
	"/management/staff": [20,[10]]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};

export { default as root } from '../root.svelte';