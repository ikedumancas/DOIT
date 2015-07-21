// Get list and list task undone
function LoadUserLists () {
	console.log("Loading user lists");
	$.ajax({
		url:LOAD_LIST_URL,
		type: 'GET',
		success: function(json) {
			$('.doit-navigation #loading-lists').css('display', 'none');
			$(json).each(function(){
				if(this.title.length > 18) {
					title = this.title.substring(0, 18) + '...';
				} else {
					title = this.title;
				}
				if(this.slug=='today') {
					$('.doit-navigation').prepend('<a title="'+ this.title +'" class="mdl-navigation__link mdl-button mdl-js-button mdl-js-ripple-effect" href="#'+ this.slug +'-list">\
						<i class="mdl-color-text--yellow-500 material-icons">grade</i>'+ title +' \
						<div class="mdl-layout-spacer"></div><div class="mdl-badge mdl-color--blue-100" data-badge="'+ this.count +'"></div></a>');
				} else if(this.slug=='in_seven_days') {
					$('.doit-navigation').prepend('<a title="'+ this.title +'" class="mdl-navigation__link mdl-button mdl-js-button mdl-js-ripple-effect" href="#'+ this.slug +'-list">\
						<i class="mdl-color-text--light-blue-500 material-icons">grade</i>'+ title +' \
						<div class="mdl-layout-spacer"></div><div class="mdl-badge mdl-color--blue-100" data-badge="'+ this.count +'"></div></a>');
				} else {
					$('.doit-navigation').prepend('<a title="'+ this.title +'" class="mdl-navigation__link mdl-button mdl-js-button mdl-js-ripple-effect" href="#'+ this.slug +'-list">\
						<i class="mdl-color-text--blue-grey-400 material-icons">list</i>'+ title +' \
						<div class="mdl-layout-spacer"></div><div class="mdl-badge mdl-color--blue-100" data-badge="'+ this.count +'"></div></a>')
				}
			});
			console.log("List loaded successfully");
		},
		error: function(xhr,errmsg,err) {
			alert("Something went wrong!")
			console.log(errmsg)
			console.log(xhr.status + ": " + xhr.responseText)
		}
	});
}

// Get list tasks
// Add list
// Edit list
// Edit title
// Add user to list
// Delete list
// Add task
// Edit task
// Delete task
// Reorder task
// Comment on task
// Assign task

$(document).ready(function(){
	console.log("Starting app.");

	// Get list and list task undone count
	LoadUserLists();
	// Get list tasks and activate tab
	// Add list
	// Edit list
	// Edit title
	// Add user to list
	// Delete list
	// Add task
	// Edit task
	// Delete task
	// Reorder task
	// Comment on task
	// Assign task ( not sure yet )
});