// sidenav
const sideNav = document.querySelectorAll('.sidenav');
M.Sidenav.init(sideNav);

// slider
const slider = document.querySelectorAll('.slider');
M.Slider.init(slider, {
	indicators: false,
	duration: 600,
	interval: 4000
});

// dropdown
const dropdown = document.querySelectorAll('.dropdown-nav')
M.Dropdown.init(dropdown, {
	coverTrigger:false,
	constrainWidth:false,
	hover:true
});

const dropdownside = document.querySelectorAll('.dropdown-sidenav')
M.Dropdown.init(dropdownside, {
	coverTrigger:false,
});

// parallax
const parallax = document.querySelectorAll('.parallax');
M.Parallax.init(parallax);

// scrollspy
const scroll = document.querySelectorAll('.scrollspy');
M.ScrollSpy.init(scroll, {
scrollOffset: 65
});




// wowjs
new WOW().init();