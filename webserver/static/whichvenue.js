$(document).ready(function() {
	$("#venue_on_change").hide();
    $("#add_time_slot").hide();
    $("#options").hide();
	$("#which_venue li").on("click",function() {
		console.log($(this).text().split(" ")[1]);
		console.log($("#username").val());
		$.ajax({
            async: false,
            type: 'post',
            url: '/getvenues',
            data: {
                username: $("#username").val(),
                vid: $(this).text().split(" ")[1]
            },
            success: function(data) {
                $("#venue_on_change").hide();
                $("#add_time_slot").hide();
                $("#options").show();
                $("#vidm").val(data);
                $("#vidmform").val(data);
                $("#vidts").val(data);
                $("#vidtsform").val(data);
            },
            error: function() {
            },
            complete: function() {
            }
        });
	})

    $("#options li").on("click",function() {
        console.log($(this).text());
        if ($(this).text()=="Edit Venue") {
            $("#add_time_slot").hide();
            $("#options").show();
            $("#venue_on_change").show();
        };
        if ($(this).text()=="Add Time Slot"){
            $("#venue_on_change").hide();
            $("#options").show();
            $("#add_time_slot").show();
        };
        // console.log($("#username").val());
        // $.ajax({
        //     async: false,
        //     type: 'post',
        //     url: '/getvenues',
        //     data: {
        //         username: $("#username").val(),
        //         vid: $(this).text().split(" ")[1]
        //     },
        //     success: function(data) {
        //         $("#options").show();
        //         $("#vidm").val(data);
        //         $("#vidmform").val(data);
        //     },
        //     error: function() {
        //     },
        //     complete: function() {
        //     }
        // });
    })
})