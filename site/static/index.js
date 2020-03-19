$(document).ready(function() {
	resize_bot_list()
	$('#list-tab').children().eq(0).addClass('active')
	$('#nav-tabContent').children().eq(0).addClass('active')
	$('.toggle-bot-view-raw').change(function() {
		let raw = $(this).is(':checked')
		let id = $(this).attr('bot-identifier')
		$('.bot-view-raw').each(function() {
			if($(this).attr('bot-identifier') != id) return
			else if(raw) $(this).show()
			else $(this).hide()
		})
		$('.bot-view-normal').each(function() {
			if($(this).attr('bot-identifier') != id) return
			else if(!raw) $(this).show()
			else $(this).hide()
		})
	})
	$('.bot-tab-button').each(function() {
		$(this).click(function() {
			window.scrollTo(0, 0)
		})
	})
	$('#create-bot-button').click(function() {
		$.post('/create', {content: "hi"})
	})
	$('.folder-filter').each(function() {
		$(this).click(function() {
			let filter = $(this).attr('folder-filter') 
			$('.question').each(function() {
				if(filter == 'all' || $(this).attr('folders').split(' ').includes(filter)) $(this).show()
				else $(this).hide()
			})
		})
	})
	$('.mark-as-answer').each(function() {
		$(this).text('Mark as answer')
		$(this).click(function() {
			if($(this).text() == 'Mark as answer') {
				$.post('/mark_as_answer', {term: $(this).attr('term'), id: $(this).attr('id')})
				$(this).text('Unmark as answer')
			} else {
				$(this).text('Mark as answer')
			}
		})
	})
})

$(window).resize(function() {
	resize_bot_list()
})

function resize_bot_list() {
	$('.bot-list').width($('.bot-list-col').width())
}