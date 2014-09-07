$(document).ready(function(){

	function updateCounter(count){
		$('input[type=hidden].inputs-counter').val(count);	
	}

	$(getInputDiv(1)).fadeIn('slow').appendTo('.inputs');
	var i = $('.single-field').size();
	updateCounter(i);
	

	$('.add-input').click(function(){
		i++;
		$(getInputDiv(i)).fadeIn('slow').appendTo('.inputs');
		updateCounter(i);
	});

	$('.remove-input').click(function(){
		if(i > 1){
			$('.single-field:last').remove();
			i--;
			updateCounter(i);
		}
	});

});