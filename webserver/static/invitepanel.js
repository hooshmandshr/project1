$(document).ready(function() {
	$("#new_invite").hide();
	$("#my_invite").hide();
	$("#navbar li").on("click",function() {
		if ($(this).text()=="Edit Invitations") {
			$("#my_invite").show();
			$("#new_invite").hide();
		};
		if ($(this).text()=="Create New Invite") {
			$("#my_invite").hide();
			$("#new_invite").show();
		};
	})
})