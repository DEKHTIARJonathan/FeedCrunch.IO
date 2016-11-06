$( document ).ready(function() {

	function getPosition(str, m, i) {
		return str.split(m, i).join(m).length;
	}

	var uri = window.location.pathname;
	var stop_uri_position = getPosition(uri, '/', 3) + 1;
	var dashboard_root_url = uri.substring(0,stop_uri_position);

	$("#dashboard-link-menu").attr("href", dashboard_root_url);
	$("#personal-info-link-menu").attr("href", dashboard_root_url + "account/info/" );
	$("#preferences-link-menu").attr("href", dashboard_root_url + "account/preferences/" );
	$("#password-link-menu").attr("href", dashboard_root_url + "account/password/" );
	$("#profile-pict-link-menu").attr("href", dashboard_root_url + "account/picture/" );
	$("#social-link-menu").attr("href", dashboard_root_url + "account/social/" );
	$("#services-link-menu").attr("href", dashboard_root_url + "account/services/" );
	$("#add-article-link-menu").attr("href", dashboard_root_url + "article/add/" );
	$("#edit-article-link-menu").attr("href", dashboard_root_url + "article/edit/" );
	$("#delete-article-link-menu").attr("href", dashboard_root_url + "article/delete/" );
	$("#contact-link-menu").attr("href", dashboard_root_url + "contact/" );
	$("#reading-sub-management").attr("href", dashboard_root_url + "reading/subscription/" );
	$("#reading-recommendation").attr("href", dashboard_root_url + "reading/recommendation/" );
	$("#my-feed-menu").attr("href", uri.substring(0,getPosition(uri, '/', 2) + 1));

	var item = $('li a[href^="' + location.pathname + '"]').first();

	if (item.length == 0){
		if (location.pathname.indexOf("/article/edit/") != -1 )
			item = $('li a[href^="/@dataradar/admin/article/edit/"]').first()
	}

	item.parent().addClass("active");

	if(!item.filter(':visible').length){
		var category_item = item.parents('div').first();
		category_item.parent().addClass('active');
		category_item.siblings('a').addClass('active');
		item.parents('div').slideDown({ duration: 350, easing: "easeOutQuart", queue: false, complete: function() {$(this).css('height', '');}});
	}

});
