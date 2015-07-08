var LIST = $('#lists-container > div')
var LIST_CONTAINER = $('#lists-container')
var LIST_TO_CLONE = $('.clone-list .todolist-panel')
var LI_ITEM_TO_CLONE = $('.clone-task .list-group-item')
var csrf_token = $('body').find('input[name=csrfmiddlewaretoken]').val()
function create_task(form){
	csrf_token = $(form).find('input[name=csrfmiddlewaretoken]').val()
	todolist = $(form).find('input[name=todolist]').val()
	title = $(form).find('input[name=title]').val()
	$.ajax({
		url:$(form).attr('action'),
		type: 'POST',
		data: { csrfmiddlewaretoken: csrf_token, title: title, todolist: todolist },
		success: function(json) {
			append_this = LI_ITEM_TO_CLONE.clone()
			append_this.attr('data-task-id', json.slug)
			append_this.find('.todo-title-text').html(json.title)
			append_this.find('.glyphicon-ok').attr('href', json.title)
			append_this.find('.glyphicon-pencil').attr('href', json.edit_url)
			append_this.find('.glyphicon-trash').attr('href', json.archive_url)
			append_this.appendTo($(form).siblings('ul'))
			$(form).find('input[name=title]').val('')
		},
		error: function(xhr,errmsg,err) {
			$.gritter.add({
				title: 'Oops! Something went wrong.',
				text: xhr.status + ": " + xhr.responseText,
				sticky: false,
				time: ''
			});
			
		}
	});
}
function create_list(form){
	new_list_title = $(form).find('#create_quick_list').val()
	csrf_token = $(form).find('input[type=hidden]').val()
	$.ajax({
		url: $(form).attr('action'),
		type: 'POST',
		data: { csrfmiddlewaretoken: csrf_token, title: new_list_title },
		success: function(json) {
			new_width = LIST_CONTAINER.width() + $('.todolist-panel').outerWidth();
			LIST_CONTAINER.width(new_width);
			append_this = LIST_TO_CLONE.clone()
			append_this.find('.panel-title-text').html(json.title)
			append_this.find('ul.list-group').attr('data-list-id', json.slug)
			append_this.find('input[type=hidden]').val(json.slug)
			append_this.appendTo(LIST_CONTAINER).css('display','block');
			$('#create_list_panel').appendTo(LIST_CONTAINER)
			$(form).find('#create_quick_list').val('')
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
$(document).ready(function(){
	$('.task-btn.glyphicon-trash, .task-btn.glyphicon-ok').on('click', function(event){
	    event.preventDefault();
	    link = $(this);
	    $.ajax({
		url: $(this).attr('href'),
		type: 'GET',
		success: function(json) {
			li = link.closest('li');
			if(json.result == 'done'){
				link.attr('href', json.link);
				link.attr('title', 'Unmark');
				li.addClass('task-done');
				link.addClass('btn-success');
				link.removeClass('btn-default');
				console.log('Done');
			}
			if(json.result == 'undone'){
				link.attr('href', json.link);
				link.attr('title', 'Mark as Done');
				li.removeClass('task-done');
				link.removeClass('btn-success');
				link.addClass('btn-default');
				console.log('Unone');
			}
			if(json.result == 'archived'){
				li.remove();
				console.log('Archived');
			}
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
	});

	$('#quick_list_form').on('submit', function(event){
	    event.preventDefault();
	    create_list(this)
	});

	$('.quick_task_form').on('submit', function(event){
	    event.preventDefault();
	    create_task(this)
	});
	// make tasks in todolist sortable
	$('.todolist .list-group').sortable({
		update: function(event, ui) {
			var slug = $(ui.item).data('task-id')
			var new_order = ui.item.index() + 1;
			console.log(slug)
			console.log(new_order)
			$.ajax({
				url: REORDER_URL,
				type: 'POST',
				data: { csrfmiddlewaretoken: csrf_token, task_slug: slug, order:new_order  },
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
	}).disableSelection();

	// set todolist container width
	var new_width = 0;
	body_width = $('body').width()*.31;
	$('.todolist-panel').each(function(){
		$(this).width(body_width)
		new_width = new_width + $(this).outerWidth();
	});
	new_width = new_width - $('.todolist-panel').outerWidth();
	LIST_CONTAINER.width(new_width);
	LIST.css('display','block')
});