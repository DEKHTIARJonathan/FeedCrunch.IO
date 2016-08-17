$('.nav-link').click(function(e) {
	e.preventDefault();

	var goto = $(this).attr('href');

	if (goto[0] == "#"){
		 $('html, body').animate({
			scrollTop: $(goto).offset().top
		}, 800);
	}
	else{
		window.location = goto;
	}
});

$(function() {
	// Highlight the active nav link.
	var url = window.location.pathname;
		url = url.slice(0, -1); // We remove the last "/"
	var filename = url.substr(url.lastIndexOf('/'));
	$('.navbar a[href$="' + filename + '"]').parent().addClass("active");
});

$(function(){
	fullpath = window.location.pathname;
	if ( fullpath == "/" ){
		$("#nav_link_logo").prop("href", "#home");
		$("#nav_link_home").prop("href", "#home");
		$("#nav_link_features").prop("href", "#features");
		$("#nav_link_pricing").prop("href", "#pricing");
	}
	else{
		$("#nav_link_logo").prop("href", "/");
		$("#nav_link_home").prop("href", "/");
		$("#nav_link_features").prop("href", "/#features");
		$("#nav_link_pricing").prop("href", "/#pricing");
		$("#li_home").removeClass("active");
	}
});
