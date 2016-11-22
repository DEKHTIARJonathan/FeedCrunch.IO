$( document ).ready(function() {


	$('.interest-checkbox').on('change', function(evt) {
		var limit = 3;
		if($('.interest-checkbox:checked').length > limit) {
			 this.checked = false;
		}
	});

});
