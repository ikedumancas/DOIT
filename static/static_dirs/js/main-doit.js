function footerGoesDown() {
	$('main').css('min-height', $('ul#nav-mobile').height()-($('footer').outerHeight()+$('header').outerHeight())-20)
}
// Get list and list task undone
function LoadUserLists () {
	console.log("Loading user's lists");
	$.ajax({
		url:getCookie('load_list_url').split('"')[1],
		type: 'GET',
		success: function(json) {
			$('#doit-list-preloader').remove();

			$(json).each(function(){
				if(this.title.length > 18) {
					title = this.title.substring(0, 18) + '...';
				} else {
					title = this.title;
				}
				if(this.slug=='today') {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-red">\
						<i class="tiny material-icons red-text">today</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				} else if(this.slug=='in7days') {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-red">\
						<i class="tiny material-icons orange-text">today</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				} else {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-red">\
						<i class="tiny material-icons teal-text">list</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				}
			});
			console.log("Lists loaded successfully");
		},
		error: function(xhr,errmsg,err) {
			alert("Something went wrong!")
			console.log(errmsg)
			// console.log(xhr.responseText);
			$('body').html("<pre>" + xhr.responseText + "</pre>");
		}
	});
}
function LoadTasksForList(slug) {
	console.log("Getting tasks for List with slug equal to " + slug);
	title =
	$.ajax({
		url:getCookie('get_task_url').split('"')[1],
		type: 'POST',
		data: { slug: slug },
		success: function(json) {

			console.log("Tasks loaded successfully!");
		},
		error: function(xhr,errmsg,err) {
			alert("Something went wrong!")
			console.log(errmsg)
			console.log(xhr.responseText);
			$('body').html("<pre>" + xhr.responseText + "</pre>");
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
	// detect resize
	$( window ).resize(function(){
		footerGoesDown();
	});

	// detect input helper
	$('body').on('focus', 'input',function(){
		$(this).siblings('.doit-input-helper-text').css('display','block');
	});

	function setCardHeightToRevealHeight(card){
		card.height(card.find('.card-reveal')[0].scrollHeight);
	}
	$('body').on('click', '.card .activator',function(){
		card = $(this).closest('.card');
		setTimeout(function(){ 
			setCardHeightToRevealHeight(card);
		}, 0);

		// card.height(card.find('.card-reveal').delay(100).scrollTop());
		
		// card.css('height', card.find('.card-reveal')[0].scrollHeight)
	});
	$('body').on('click', '.card .deactivator',function(){
		card = $(this).closest('.card')
		card.css('height', '')
	})
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