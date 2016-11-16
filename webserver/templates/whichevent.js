$(document).ready(function() {
	$("#event_on_change").hide();
    $("#options").hide();
	$("#which_event li").on("click",function() {
		$("#selected_event_invite").val($(this).text().split(" ")[1]);
        $("#selected_event_edit").val($(this).text().split(" ")[1]);
        $("#selected_event_request").val($(this).text().split(" ")[1]);
        $("#selected_event_inventory").val($(this).text().split(" ")[1]);
        $("#options").show();
        $("#event_on_change").hide();
	})

    $("#options button").on("click",function() {
        if ($(this).text()=="Edit Event") {
            $("#options").show();
            $("#event_on_change").show();
            var selected="#"+"event_on_change"+$("#selected_event_invite").val();
            $(selected).show().find('input, textarea').prop('disabled', false);
            var events={{events|tojson}};
            $.each( events, function( key, value ) {
                if (key!=$("#selected_event_invite").val()) {
                    var notselected="#"+"event_on_change"+key;
                    $(notselected).hide().find('input, textarea').prop('disabled', true);
                }
            })
        };
    })
})