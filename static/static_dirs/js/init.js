(function($){
  $(function(){
  	console.log("Initializing...");
    footerGoesDown()
  	// Set sideNav
    $('.button-collapse').sideNav({ edge:'left' });
  	LoadUserLists();
  	// Get Today List
  	setTimeout(function() {
  	  LoadTasksForList('today');
  	}, 0);
  });
})(jQuery);