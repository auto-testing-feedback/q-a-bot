$('#submitError').attr('hidden', '')
$('#submit').click(function() {
	let title1 = $('#title1').val().trim()
	let title2 = $('#title2').val().trim()
	let content1 = $('#content1').val().trim()
	let content2 = $('#content2').val().trim()

	if(content1.length == 0 || content2.length == 0) {
		$('#submitError').removeAttr('hidden')
		$('#output').attr('hidden', '')
	} else {
		$('#submitError').attr('hidden', '')
		$.get('/matcher-demo/query', {
			'title1': title1,
			'title2': title2,
			'content1': content1,
			'content2': content2
		}, function(data, status) {
			$('#output').removeAttr('hidden')
			$('#output').html(JSON.stringify(data))
		})
	}
})