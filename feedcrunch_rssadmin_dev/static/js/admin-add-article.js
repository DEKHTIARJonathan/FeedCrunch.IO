$( document ).ready(function() {
	var validator = $("#add-form").validate({
		debug: true
	});


	$("#submit").click(function() {
		swal({
			title: "Good job!",
			text: "Article Submitted!",
			type: "success",
			timer: 1500,
			showConfirmButton: false,
		});
	});

	$("#reset").click(function() {
		swal({
			title: "Are you sure?",
			text: "You will not be able to recover this imaginary file!",
			type: "warning",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes, delete it!",
			closeOnConfirm: false
		},
		function(){
			swal("Deleted!", "Your imaginary file has been deleted.", "success");
		});
	});

});
