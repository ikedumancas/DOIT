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
						<a href="#'+ this.slug +'-list" class="waves-effect waves-red doit-list-select">\
						<i class="tiny material-icons red-text">today</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				} else if(this.slug=='in7days') {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-orange doit-list-select">\
						<i class="tiny material-icons orange-text">today</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				} else if(this.slug=='overdue') {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-red doit-list-select">\
						<i class="tiny material-icons red-text">list</i> '+ title +'<span class="badge">'+ this.count +'</span></a></li>');
				} else {
					$('#nav-mobile .logo').after('<li title="'+ this.title +'" class="bold no-padding">\
						<a href="#'+ this.slug +'-list" class="waves-effect waves-teal doit-list-select">\
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
// Get list tasks
function LoadTasksForList(slug) {
	var slug_to_load = slug;
	console.log("Getting tasks for List with slug equal to " + slug_to_load);
	$.ajax({
		url:getCookie('get_task_url').split('"')[1],
		type: 'POST',
		data: { slug: slug_to_load },
		success: function(json) {
			console.log("Loading Tasks...");
			var container = $('#doit-container')
			container.html('');
			if(slug_to_load == 'today' || slug_to_load == 'in7days'){
				if(slug_to_load == 'today'){
					$('header>.top-nav .page-title').html("Today");
				}else {
					$('header>.top-nav .page-title').html("Next 7 days");
				}
			} else {
				$('header>.top-nav .page-title').html(json[0].list.list_title);
			}
			var first_iteration = true;
			if(json.length > 0) {
				$(json).each(function(){
					var template_clone = $('#doit-template').clone();
					template_clone.attr('id', this.list.todo.slug + '-todo');
					template_clone.addClass('priority-'+this.list.todo.priority);
					template_clone.find('.doit-title').html(this.list.todo.title);
					template_clone.find('.doit-task-status').attr('data-url',this.list.todo.done_url);
					template_clone.find('.doit-task-edit').attr('data-url',this.list.todo.edit_url);
					template_clone.find('.doit-task-delete').attr('data-url',this.list.todo.archive_url);
					if(!this.list.todo.is_active) {
						template_clone.addClass('light-blue accent-3 white-text');
						template_clone.find('.doit-task-status').removeClass('waves-green white').addClass('waves-light green');
						template_clone.find('.doit-task-status .material-icons').removeClass('grey-text');
					}
					if(!this.list.todo.has_description) {
						template_clone.find('.doit-has-description').remove();
					}
					if(this.list.todo.comment_count){
						template_clone.find('.doit-has-comment doit-comment-count').html(this.list.todo.comment_count);
					}else{
						template_clone.find('.doit-has-comment').remove();
					}
					if(this.list.todo.due_date){
						if(this.list.todo.due_date.status != 'default'){
							if(this.list.todo.is_active){
								if(this.list.todo.due_date.status == 'warning'){
									template_clone.find('.doit-has-duedate').removeClass('grey').addClass('orange');
								}else {
									template_clone.find('.doit-has-duedate').removeClass('grey').addClass('red');
								}
							}
						}
						if(this.list.todo.due_date.overdue) {
							if(!this.list.todo.is_active){
								template_clone.find('.doit-duedate').html(this.list.todo.due_date.date+' ago');
							}else {
								template_clone.find('.doit-duedate').html(this.list.todo.due_date.date+' overdue');
							}
						}else{
							template_clone.find('.doit-duedate').html(this.list.todo.due_date.date);
						}
					}else{
						template_clone.find('.doit-has-duedate').remove();
					}
					// change display css
					template_clone.css('display','');
					// Append to list
					container.append(template_clone);
				});
				if(slug_to_load != 'today' && slug_to_load != 'in7days' && slug_to_load != 'overdue'){
					$('#doit-container').sortable({
						update: function(event, ui) {
							var slug = $(ui.item).attr('id').split('-todo')[0];
							var new_order = ui.item.index() + 1;
							reorder_list_tasks(slug,new_order)
						}
					}).disableSelection();
				}
			} else {
				container.html('<h3>No tasks to load.</h3>')
			}
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
// Add list
// Edit list
// Edit title
// Add user to list
// Delete list
// Add task
// Edit task
// Delete task
// Reorder task
function reorder_list_tasks(slug,new_order){
	$.ajax({
		url: getCookie('reorder_url').split('"')[1],
		type: 'POST',
		data: { task_slug: slug, order:new_order  },
		success: function(json) {
			console.log('List Reordered');
		},
		error: function(xhr,errmsg,err) {
			$.gritter.add({
				title: 'Oops! Something went wrong.',
				sticky: false,
				time: ''
			});
			console.log(errmsg)
			console.log(xhr.status + ": " + xhr.responseText)
		}
	});
}
// Comment on task
// Assign task

$(document).ready(function(){
	console.log("Starting app.");
	// detect resize
	$( window ).resize(function(){
		footerGoesDown();
	});

	// input helper
	$('body').on('focus', 'input',function(){
		$(this).siblings('.doit-input-helper-text').fadeIn();
	});
	$('body').on('blur', 'input',function(){
		$(this).siblings('.doit-input-helper-text').fadeOut();
	});


	// detect list clicked
	$('body').on('click', '.doit-list-select', function(){
		slug = $(this).attr('href').split('#')[1].split('-list')[0]
		LoadTasksForList(slug);
	});
	// detect task clicked
	$('body').on('click', '.card', function(){
		// get tasks detail ajax;
		// display modal with data from ajax
	});
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