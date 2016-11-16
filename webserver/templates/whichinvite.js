$(document).ready(function() {
	$("#invite_on_change").hide();
	$("#which_invite li").on("click",function() {
        $("#invite_on_change").show();
        var which=$(this).text().split(" ")[1];
        console.log(which);
        var selected="#"+"invite_on_change"+which;
        // console.log(selected);
        $(selected).show().find('input, textarea').prop('disabled', false);
        var invite={{invite|tojson}};
        $.each( invite, function( key, value ) {
            // console.log(key+":"+value);
            if (key!=which) {
                console.log(key+":"+which);
                var notselected="#"+"invite_on_change"+key;
                $(notselected).hide().find('input, textarea').prop('disabled', true);
            }
        });
	});
});