$(document).ready(function(){
	var doc = $(document),
		navbar = $('.navbar'),
		threshold = (parseInt(navbar.next().offset().top) - parseInt(navbar.height()));

	doc.scroll(function() {
		navbar.toggleClass('overlap', (window.pageYOffset || document.documentElement.scrollTop) >= threshold);
	});
})