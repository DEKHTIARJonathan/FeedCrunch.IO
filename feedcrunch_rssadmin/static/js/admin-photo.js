$( document ).ready(function() {

	function clearFields(){
		$(".file-path").val("");
		$("#photo").val("");
	}

	function showError(error){
		swal({
			title: "Something went wrong!",
			text: error,
			type: "error",
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "I'll retry later",
			closeOnConfirm: true
		});
	}

	$("#reset-btn").click(function() {
		swal({
			title: "Are you sure ?",
			text: "Do you really want to reset all the fields ?",
			type: "warning",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes, please reset!",
			cancelButtonText: "Please No!",
			closeOnConfirm: true,
			closeOnCancel: true
		}, function(){
			clearFields();
			swal.close();
		});
	});

	$("#save-btn").click(function() {
		var csrftoken = Cookies.get('csrftoken');

		allowed_mime_types = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/png'];

		var photo_data = new FormData();
		photo_data.append("photo", $("#photo").val());

		photo = $('#photo').prop('files')[0];

		if (jQuery.inArray(photo.type,  allowed_mime_types) == -1)
			showError("Only GIF, PNG and JPEG files are allowed.");

		else if(photo.size > 1048576)
			showError("Uploaded File too big. Maximum Filesize allowed: 1MB.");
		else {
			$("#form-photo").submit();
		}

	});

});
