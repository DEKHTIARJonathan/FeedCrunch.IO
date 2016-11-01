$( document ).ready(function() {

	form_fields = [
		'old_password',
		'new_password_1',
		'new_password_2',
	]

	function clearFields(){
		for (field in form_fields){
			//console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
			var input = $("#"+form_fields[field]);
			input.val("");
		}
	}

	function get_fields(){
		var rslt = {};
		for (field in form_fields){
			//console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
			var input = $("#"+form_fields[field]);
			rslt[form_fields[field]] = input.val();
		}
		return rslt;
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
		var api_url = "/api/1.0/authenticated/modify/user/password/";
		var csrftoken = Cookies.get('csrftoken');

		$.ajax({
			url : api_url,
			type : "PUT",
			data: get_fields(),
			dataType : "json",
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(data){
				if (data.success) {
					swal({
						title: "Good job!",
						text: "Password modified with success!",
						type: "success",
						timer: 1500,
						showConfirmButton: false,
						cache: false,
					}, function(){
						clearFields();
						swal.close();
					});
				}
				else {
					swal({
						title: "Something went wrong!",
						text: data.error,
						type: "error",
						confirmButtonColor: "#DD6B55",
						confirmButtonText: "I'll retry later",
						closeOnConfirm: true
					});
				}
			}
		});
	});

});
