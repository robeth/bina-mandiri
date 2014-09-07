$(document).ready(function(){
	$("#adv-window").hide();
	$("#adv-button").click(function(){
		if ($(this).hasClass("active")){
			$(this).removeClass("active");
			$("#adv-window").slideUp();
		} else {
			$(this).addClass("active");
			$("#adv-window").slideDown();
		}
	});
});