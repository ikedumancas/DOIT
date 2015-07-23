(function($){
  $(function(){
  	// Set sideNav
    $('.button-collapse').sideNav({ edge:'left' });

    // Footer to the bottom of the page
    footerGoesDown()
	
    // Get list and list task undone count
	LoadUserLists();

	// Get Today List
	LoadTasksForList('today');

  }); // end of document ready
})(jQuery); // end of jQuery name space