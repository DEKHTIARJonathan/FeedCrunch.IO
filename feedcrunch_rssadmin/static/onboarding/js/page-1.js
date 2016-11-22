$( document ).ready(function() {


	$('.interest-checkbox').on('change', function(evt) {
		var limit = 3;
		var amount_checked = $('.interest-checkbox:checked').length;
		if(amount_checked > limit) {
			this.checked = false;
		}
		else if (amount_checked == limit) {
			$(".continue").prop("disabled", false);
			$(".continue").html("Continue &rarr;");
		}
		else{
			$(".continue").prop("disabled", true);
			$(".continue").html("Select 3 to Continue");
		}
	});

});
