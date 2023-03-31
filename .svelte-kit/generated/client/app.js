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
	() => import('./nodes/22'),
	() => import('./nodes/23'),
	() => import('./nodes/24'),
	() => import('./nodes/25'),
	() => import('./nodes/26')];

export const server_loads = [];

export const dictionary = {
	"/": [14],
	"/auth": [15,[2]],
	"/basket": [16,[3]],
	"/bookings": [17,[4]],
	"/cancel": [18,[5]],
	"/dashboard": [19,[6]],
	"/employees/amend": [20,[7]],
	"/employees/book": [21,[8]],
	"/management/activities": [22,[9]],
	"/management/analytics": [23,[10]],
	"/management/facilities": [24,[11]],
	"/management/staff": [25,[12]],
	"/success": [26,[13]]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};

export { default as root } from '../root.svelte';