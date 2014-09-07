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

	function updateCounter2(count){
		$('input[type=hidden].inputs-counter2').val(count);	
	}

	$(getInputDiv2(1)).fadeIn('slow').appendTo('.inputs2');
	var j = $('.single-field2').size();
	updateCounter2(j);
	

	$('.add-input2').click(function(){
		j++;
		$(getInputDiv2(j)).fadeIn('slow').appendTo('.inputs2');
		updateCounter2(j);
	});

	$('.remove-input2').click(function(){
		if(j > 1){
			$('.single-field2:last').remove();
			j--;
			updateCounter2(j);
		}
	});

});