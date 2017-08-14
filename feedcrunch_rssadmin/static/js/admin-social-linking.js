$(document).ready(function() {

	var interval;

    var social_networks_dict = {
        twitter:  "#twitter-btn-div",
        facebook: "#facebook-btn-div",
        linkedin: "#linkedin-btn-div",
    };

	function checkSocialNetworkStatus(social_network) {

        if (Object.keys(social_networks_dict).indexOf(social_network) == -1){
            console.log("This social network is not supported: " + social_network);
            return False;
        }

		$.ajax({
			type: 'GET',
			url: '/api/1.0/authenticated/get/user/social-networks/'+social_network+'/status/',
			dataType: 'json',
			success: function(data){
				if (data.success) {
					if (data.status){
                        $(social_networks_dict[social_network]).html(
                            `<button class="waves-effect waves-light btn red socialconnect-btn" id="`+social_network+`-btn-unlink">
                                Unlink My `+social_network[0].toUpperCase() + social_network.slice(1)+` Account
                            </button>`
                        );
						setUnlinkClickEvent();
					}
					else
            			interval = setTimeout(function() {
                            checkSocialNetworkStatus(social_network);
                        }, 1500);
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

    function UnLinkSocialNetwork(social_network) {
        var csrftoken = Cookies.get('csrftoken');

        if (Object.keys(social_networks_dict).indexOf(social_network) == -1){
            console.log("This social network is not supported: " + social_network);
            return False;
        }

        $.ajax({
            type: 'DELETE',
            url: '/api/1.0/authenticated/delete/user/social-networks/'+social_network+'/',
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                if (data.success) {
                    $(social_networks_dict[social_network]).html(
                        `<a href="`+ data.auth_url +`"  target="_target" class="waves-effect waves-light btn blue socialconnect-btn" id="`+social_network+`-btn-link">
                            Link My `+social_network[0].toUpperCase() + social_network.slice(1)+` Account
                        </a>`
                    );
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
        $("#twitter-btn-link").unbind("click");
		$("#twitter-btn-link").click(function() {
			interval = setTimeout(function() {
                checkSocialNetworkStatus("twitter");
            }, 1500);
		});

        $("#facebook-btn-link").unbind("click");
        $("#facebook-btn-link").click(function() {
			interval = setTimeout(function() {
                checkSocialNetworkStatus("facebook");
            }, 1500);
		});

        $("#linkedin-btn-link").unbind("click");
        $("#linkedin-btn-link").click(function() {
			interval = setTimeout(function() {
                checkSocialNetworkStatus("linkedin");
            }, 1500);
		});

	}

	function setUnlinkClickEvent() {
        $("#twitter-btn-unlink").unbind("click");
		$("#twitter-btn-unlink").click(function(event) {
            UnLinkSocialNetwork("twitter");
            event.preventDefault();
            return false;
        });

        $("#facebook-btn-unlink").unbind("click");
        $("#facebook-btn-unlink").click(function(event) {
            UnLinkSocialNetwork("facebook");
            event.preventDefault();
            return false;
        });

        $("#linkedin-btn-unlink").unbind("click");
        $("#linkedin-btn-unlink").click(function(event) {
            UnLinkSocialNetwork("linkedin");
            event.preventDefault();
            return false;
        });

	}

	setLinkClickEvent();
	setUnlinkClickEvent();

});
