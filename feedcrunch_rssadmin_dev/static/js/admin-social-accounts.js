$( document ).ready(function() {

	var social_networks = social_networks = [
		'dribbble',
		'facebook',
		'flickr',
		'gplus',
		'instagram',
		'linkedin',
		'pinterest',
		'stumble',
		'twitter',
		'vimeo',
		'youtube',
		'docker',
		'git',
		'kaggle',
		'coursera',
		'googlescholar',
		'orcid',
		'researchgate',
		'blog',
		'website'
	];

	function clearFields(){
		for (field in social_networks){
			//console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
			var input = $("#"+social_networks[field]);
			input.val(input.data("init"));
		}
	}

	function get_fields(){
		var rslt = {};
		for (field in social_networks){
			//console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
			var input = $("#"+social_networks[field]);
			rslt[social_networks[field]] = input.val();
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
		var api_url = "/api/1.0/authenticated/modify/social-networks/";
		var csrftoken = Cookies.get('csrftoken');

		console.log();

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
						text: "Social Networks modified with success!",
						type: "success",
						timer: 1500,
						showConfirmButton: false,
						cache: false,
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
