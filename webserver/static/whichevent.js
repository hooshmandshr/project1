$(document).ready(function() {
	$("#event_on_change").hide();
	$("#which_event li").on("click",function() {
		console.log($(this).text().split(" ")[1]);
		console.log($("#username").val());
		$.ajax({
            async: false,
            type: 'post',
            url: '/getevents',
            data: {
                username: $("#username").val(),
                eid: $(this).text().split(" ")[1]
            },
            success: function(data) {
                $("#event_on_change").show();
                $("#eid").val(data);
                $("#eidform").val(data);
            },
            error: function() {
            },
            complete: function() {
            }
        });
	})
})