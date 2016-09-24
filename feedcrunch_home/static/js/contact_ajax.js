function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

$('.btn-submit').click(function() {
	$(".text-success").hide();
	$(".error").hide();
	$.ajax({
        url: "https://formspree.io/contact@dataradar.io",
        method: "POST",
        data: {
			name: $("#name").val(),
			email: $("#email").val(),
			message: $("#message").val(),
			_subject: $("#_subject").val(),
			_gotcha: $("#_gotcha").val()
		},
        dataType: "json",
		beforeSend: function() {
			if ($("#name").val().length < 5){
				$(".error").text("The Name should be longer than 5 characters !");
				$(".error").show();
				return false;
			}

			if( !validateEmail($("#email").val())){
				$(".error").text("The Email Address is not valid !");
				$(".error").show();
				return false;
			}

			if ($("#message").val().length < 30){
				$(".error").text("The Message should be longer than 30 characters !");
				$(".error").show();
				return false;
			}

			return true;

		},
		success: function (data) {
			if (data.success == "email sent") {
				$(".text-success").show();
			} else {
				$(".error").text("Error while sending the email");
				$(".error").show();
			}
			$("#name").val("");
			$("#email").val("")
			$("#message").val("");
		},
		error: function() {
			$(".error").text("Error while sending the email - Impossible to contact the host.");
			$(".error").show();
        }
    });
   return false; // prevent default
 });
