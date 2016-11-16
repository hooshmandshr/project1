function emptycheck (line, element) {
	if (!$("#"+element).val()) {
		line.push(element);
	};
	return line;
}

function checkValidation () {
	var invalidfield=[];
	invalidfield=emptycheck(invalidfield,"username")
	invalidfield=emptycheck(invalidfield,"firstname")
	invalidfield=emptycheck(invalidfield,"lastname")
	invalidfield=emptycheck(invalidfield,"password")
	invalidfield=emptycheck(invalidfield,"dob")
	invalidfield=emptycheck(invalidfield,"address")
	invalidfield=emptycheck(invalidfield,"email")
	invalidfield=emptycheck(invalidfield,"phone")
	return invalidfield;
}

$(document).ready(function() {
	$("#register").on("submit", function() {
		var validation = checkValidation();
		if (validation.length!=0) {
			alert("Please fill in "+validation);
			return false;
		}
		else{
			return true;
		}
	})
})