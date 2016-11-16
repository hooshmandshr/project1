$(document).ready(function() {
	$("#new_venue").hide();
	$("#my_venue").hide();
	$("#navbar li").on("click",function() {
		if ($(this).text()=="Manage Venue") {
			$("#my_venue").show();
			$("#new_venue").hide();
		};
		if ($(this).text()=="Register Venue") {
			$("#my_venue").hide();
			$("#new_venue").show();
		};
	})
})