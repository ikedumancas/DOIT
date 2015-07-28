(function($){
  $(function(){
  	console.log("Initializing...");
    footerGoesDown()
  	// Set sideNav
    $('.button-collapse').sideNav({ edge:'left' });
  	LoadUserLists();
  	// Get Today List
  	setTimeout(function() {
      if(window.location.hash ==""){
  	   LoadTasksForList('today'); 
      } else {
        slug = window.location.hash.split('#')[1].split('-list')[0];
        LoadTasksForList(slug); 
      }
  	}, 0);
  });
})(jQuery);