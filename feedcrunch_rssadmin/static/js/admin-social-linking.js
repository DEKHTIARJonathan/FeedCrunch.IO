$(document).ready(function() {

	var interval;

	function checkTwitterLinkStatus() {
		$.ajax({
			type: 'GET',
			url: '/api/1.0/authenticated/get/user/social-networks/twitter/status/',
			dataType: 'json',
			success: function(data){
				if (data.success) {
					if (data.status){
						$("#twitter-btn-div").html('<button class="waves-effect waves-light btn red twitter-btn" id="twitter-btn-unlink">Unlink My Twitter Account</button>');
						setUnlinkClickEvent();
					}
					else
						interval = setTimeout(checkTwitterLinkStatus, 1500);
				}
				else{
					swal({
						title: "Something went wrong!",
						text: data.error,
						type: "error",
						confirmButtonColor: "#DD6B55",
						confirmButtonText: "I'll Fix it!",
						closeOnConfirm: true
					});
				}
			}
		});
	}

    function UnLinkTwitter() {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            type: 'DELETE',
            url: '/api/1.0/authenticated/delete/user/social-networks/twitter/',
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                if (data.success) {
                    $("#twitter-btn-div").html('<a href="' + data.auth_url + '" target="_target" class="waves-effect waves-light btn blue" id="twitter-btn-link">Link My Twitter Account</a>');
                    setLinkClickEvent();
                }
                else{
                    swal({
                        title: "Something went wrong!",
                        text: data.error,
                        type: "error",
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "I'll Fix it!",
                        closeOnConfirm: true
                    });
                }
            }
        });
    }

    function checkFacebookLinkStatus() {
		$.ajax({
			type: 'GET',
			url: '/api/1.0/authenticated/get/user/social-networks/facebook/status/',
			dataType: 'json',
			success: function(data){
				if (data.success) {
					if (data.status){
						$("#facebook-btn-div").html('<button class="waves-effect waves-light btn red twitter-btn" id="facebook-btn-unlink">Unlink My Facebook Account</button>');
						setUnlinkClickEvent();
					}
					else
						interval = setTimeout(checkFacebookLinkStatus, 1500);
				}
				else{
					swal({
						title: "Something went wrong!",
						text: data.error,
						type: "error",
						confirmButtonColor: "#DD6B55",
						confirmButtonText: "I'll Fix it!",
						closeOnConfirm: true
					});
				}
			}
		});
	}

    function UnLinkFacebook() {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            type: 'DELETE',
            url: '/api/1.0/authenticated/delete/user/social-networks/facebook/',
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                if (data.success) {
                    $("#facebook-btn-div").html('<a href="' + data.auth_url + '"  target="_target" class="waves-effect waves-light btn blue" id="facebook-btn-link">Link My Facebook Account</a>');
                    setLinkClickEvent();
                }
                else{
                    swal({
                        title: "Something went wrong!",
                        text: data.error,
                        type: "error",
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "I'll Fix it!",
                        closeOnConfirm: true
                    });
                }
            }
        });
    }

    /* ========================== Event Callbacks ***************************** */

	function setLinkClickEvent() {
		$("#twitter-btn-link").click(function() {
			interval = setTimeout(checkTwitterLinkStatus, 5000);
		});
        $("#facebook-btn-link").click(function() {
			interval = setTimeout(checkFacebookLinkStatus, 5000);
		});
	}

	function setUnlinkClickEvent() {
		$("#twitter-btn-unlink").click(function(event) {
            UnLinkTwitter();
            event.preventDefault();
            return false;
        });

        $("#facebook-btn-unlink").click(function(event) {
            UnLinkFacebook();
            event.preventDefault();
            return false;
        });
	}

	setLinkClickEvent();
	setUnlinkClickEvent();

});
