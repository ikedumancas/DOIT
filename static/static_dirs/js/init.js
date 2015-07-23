(function($){
  $(function(){
  	console.log("Initializing...");
    footerGoesDown()
  	// Set sideNav
    $('.button-collapse').sideNav({ edge:'left' });

    // Footer to the bottom of the page
	// LoadUserLists();
	// LoadTasksForList('today');
	
    // Get list and list task undone count
    // $.when(LoadUserLists()).done(LoadTasksForList('today'));
	LoadUserLists();
	// Get Today List
	setTimeout(function() {
	  LoadTasksForList('today');
	}, 0);

  }); // end of document ready
})(jQuery); // end of jQuery name space