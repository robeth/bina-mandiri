$(document).ready(function(){

	$('body [href^=#]').click(function (e) {
		e.preventDefault()
	})

	$('[data-toggle=tooltip]').tooltip()

});