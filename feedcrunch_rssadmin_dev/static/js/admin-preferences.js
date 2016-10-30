$( document ).ready(function() {

	var dashboard_link = window.location.pathname.split("/",3).join("/") + "/";
	var feed_link = window.location.pathname.split("/",2).join("/") + "/";

	$("#dashboard-btn").attr("href", dashboard_link);
	$("#feed-btn").attr("href", feed_link);

});
