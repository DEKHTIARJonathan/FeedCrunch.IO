$(document).ready(function(){
	$("#trigger-nav-overlay, .overlay-close").click(function() {
		toggleOverlay();
		$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').toggleClass('open');
	});

});
$(document).keyup(function(e) {
	if( $('.overlay').hasClass('open') ) {
	  if (e.keyCode == 27) { // escape key maps to keycode `27`
	    toggleOverlay();
	  }
	}
});

function toggleOverlay() {
	if( $('.overlay').hasClass('open') ) {
		$('.overlay').removeClass('open');
		$('.overlay').addClass('closed');
		$('.wrapper').removeClass('blur');
	}
	else if( !$('.overlay').hasClass('open') ) {
		$('.overlay').removeClass('closed');
		$('.overlay').addClass('open');
		$('.wrapper').addClass('blur');
	}
}

