$(document).ready(function() {
	$("#my_event").hide();
	$("#new_event").hide();
	$("#navbar li").on("click",function() {
		if ($(this).text()=="My Events") {
			$("#my_event").show();
			$("#new_event").hide();
		};
		if ($(this).text()=="Create Event") {
			$("#my_event").hide();
			$("#new_event").show();
		};
	})
})