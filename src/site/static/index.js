$(document).ready(function() {
	let first_identifier = $('#list-tab').children().first().attr('identifier')
	$('#list-tab').children().first().addClass('active')
	$('#data-col').children().first().removeAttr('hidden')

	$('.bot-list-group').children().each(function() {
		$(this).click(function() {
			let identifier = $(this).attr('identifier')
			$('#data-col').children().each(function() {
				if($(this).attr('identifier') === identifier) {
					$(this).removeAttr('hidden')
				} else {
					$(this).attr('hidden', '')
				}
			})
		})
	})

	$('#piazza-view').removeAttr('hidden')
	$('#data-views').change(function() {
		let data_view = $('#data-views').val();
		$('#data-views').children().each(function() {
			let view = $(this).attr('value') 
			if(data_view === view) {
				$('#' + view + '-view').removeAttr('hidden')
			} else {
				$('#' + view + '-view').attr('hidden', '')
			}
		})
	})
})