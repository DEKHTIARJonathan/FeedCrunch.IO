$(document).ready(function() {

	var table = $('#sub-listing').DataTable({
		"columns": [
			{ "searchable": false},
			null,
			null,
			null,
			{ "searchable": false},
			{ "searchable": false},
			{ "searchable": false},
		],
		"pageLength": 50, // 50 values display by page
		"lengthChange": false, // no dropdown displayed
		responsive: true,
		"sDom": 'rt<"bottom"lp><"clear">',
		"ordering": false,
		fixedHeader: {
			header: true,
			footer: false
		},
		language: {
			oPaginate: {
				sFirst: '<i class="material-icons">chevron_left</i>',
				sPrevious: '<i class="material-icons">chevron_left</i>',
				sNext: '<i class="material-icons">chevron_right</i>',
				sLast: '<i class="material-icons">chevron_right</i>'
			},
		}
	});

	table.on( 'draw', function () {
		var body = $( table.table().body() );

		body.unhighlight();
		if ( table.rows( { filter: 'applied' } ).data().length ) {
			body.highlight( table.search() );
		}

		reset_click_delete();
		reset_click_edit();
	} );

	$("#sub-searchbar").on('input',function(e){
		table.search( $(this).val() ).draw();
	});

	function responsive_columns () {
		width = $( window ).width();

		if (width < 1200) {
			table.column( 0 ).visible( false ); // hide ID
			table.column( 2 ).visible( false ); // hide domain
			table.column( 3 ).visible( false ); // hide link
			table.column( 4 ).visible( false ); // hide articles count
		}
		else if (width < 1500) {
			table.column( 0 ).visible( false ); // hide ID
			table.column( 2 ).visible( true ); // show domain
			table.column( 3 ).visible( false ); // hide link
			table.column( 4 ).visible( false ); // hide articles count
		}
		else {
			table.column( 0 ).visible( true ); // show ID
			table.column( 2 ).visible( true ); // show domain
			table.column( 3 ).visible( true ); // show link
			table.column( 4 ).visible( true ); // show articles count
		}
		table.responsive.rebuild();
		table.responsive.recalc();
	};

	responsive_columns ();

	$( window ).resize(function() {
		responsive_columns ();
	});

	$('.dataTables_length select').addClass('browser-default');

	// ================================================================ OPML MODAL ========================================================

	form_fields_opml = [
		'opml-file',
		'opml-text-file',
	]

	function clearFields_opml(){
		for (field in form_fields_opml){
			$("#"+form_fields_opml[field]).val("");
		}
	}

	$("#close-btn-opml").click(function(){
		clearFields_opml();
	});

	$("#reset-btn-opml").click(function() {
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
			clearFields_opml();
			swal.close();
		});
	});

	// ================================================== DELETE Feed ==================================================

	function reset_click_delete(){

		$(".delete-feed").click( function(){

			var current_row = $(this);
			var feed_id = $(this).data("id");

			var api_url = "/api/1.0/authenticated/delete/rssfeed/"+feed_id+"/";
			var csrftoken = Cookies.get('csrftoken');


			swal({
				title: "Are you sure ?",
				text: "Do you really want to delete this RSS Feed ?",
				type: "warning",
				showCancelButton: true,
				confirmButtonColor: "#DD6B55",
				confirmButtonText: "Yes, please delete!",
				cancelButtonText: "Please No!",
				closeOnConfirm: true,
				closeOnCancel: true
			}, function(){
				$.ajax({
					url : api_url,
					type : "DELETE",
					data: {},
					dataType : "json",
					beforeSend: function(xhr) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					},
					success: function(data){
						if (data.success) {
							swal({
								title: "Good job!",
								text: "RSS Feed deleted with success!",
								type: "success",
								timer: 1000,
								showConfirmButton: false,
								cache: false,
							}, function() {
								table.row( current_row.parents('tr') ).remove().draw();
								swal.close();
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
				swal.close();
			});

		});
	}

	reset_click_delete();

	// =================================================== RSS Feed ADD / EDIT ====================================================

	/* ########################## Trigger Function ##################### */

	$(".add-rssfeed-btn").click(function(){
		var feed_id = "-1";
		var feed_title = "";
		var feed_link = "";

		modal_rssfeed_handler(feed_id, feed_title, feed_link);

	});

	function reset_click_edit(){

		$(".edit-rssfeed-btn").click(function(){

			var feed_id = $(this).data("id");
			var feed_title = $(this).data("title");
			var feed_link = $(this).data("link");

			modal_rssfeed_handler(feed_id, feed_title, feed_link);

		});
	}

	reset_click_edit();

	/* ########################## Modal Toggle Handler ##################### */

	function modal_rssfeed_handler(id, title, link){
		var info_div = $("#link-ajax-rslt");

		var label_title = $("#rssfeed_title").siblings('label');
		var label_link = $("#rssfeed_link").siblings('label');

		$("#rssfeed_title").val(title);
		$("#rssfeed_title").data('init',title);

		$("#rssfeed_link").val(link);
		$("#rssfeed_link").data('init',link);

		$("#rssfeed_id").val(id);
		$("#rssfeed_id").data('init',id);

		info_div.html("&emsp;");
		info_div.attr("class", "");

		if (id == "-1"){
			$("#modal-rss-header").text("Subscribe to a new RSS Feed !");

			$("#reload-info").text("Once submitted, please refresh the page to make the feed appear in the listing.");
			$($("#reload-info").parents("div")[0]).css("margin-top", "40px");

			if (label_title.hasClass( "active" ))
				label_title.removeClass("active");

			if (label_link.hasClass( "active" ))
				label_link.removeClass("active");
		} else {
			$("#modal-rss-header").text("Edit your RSS Subscribtion !");

			$("#reload-info").text("");
			$($("#reload-info").parents("div")[0]).css("margin-top", "0px");

			if (! label_title.hasClass( "active" ))
				label_title.addClass("active");

			if (! label_link.hasClass( "active" ))
				label_link.addClass("active");
		}

	}

	/* ########################## RSS Validation ##################### */

	function isUrlValid(url) {
		return /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url);
	}

	$('#rssfeed_link').on('paste', function (){
		setTimeout($.proxy(function () {
			$(this).blur();
		}, this), 100);
	});

	$('#rssfeed_link').on('change',function (){

		var rss_link_input = $(this).val();
		var rss_link_init_value = $(this).data('init');

		var api_url = "/api/1.0/public/post/validate/rssfeed/";
		var csrftoken = Cookies.get('csrftoken');

		var info_div = $("#link-ajax-rslt");
		var label = $("#rssfeed_title").siblings('label');
		var title_div = $("#rssfeed_title");

		if (! isUrlValid(rss_link_input) ){ // URL empty or not valid
			info_div.html("&emsp;");
			info_div.attr("class", "");
			return false;
		}

		if ( rss_link_input ==  rss_link_init_value){ // URL is back to init value
			info_div.html("&emsp;");
			info_div.attr("class", "");
			return false;
		}

		$.ajax({
			url : api_url,
			type : "POST",
			data: {
				rssfeed: rss_link_input,
			},
			timeout: 5000, // sets timeout to 5 seconds
			dataType : "json",
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
				info_div.text("Validating your input ...");
				info_div.attr("class", "green-text text-darken-2");
				if (label.hasClass( "active" )){
					label.removeClass("active");
					title_div.val("");
				}
			},
			error: function(jqXHR, textStatus){
				if(textStatus === 'timeout')
				{
					info_div.text("Request Timeout, please try again...");
					info_div.attr("class", "red-text text-darken-2");
				}
			},
			success: function(data){
				if (data.success && data.valid) {
					if (! label.hasClass( "active" ))
						label.addClass("active");

					title_div.val(data.title);

					info_div.html("&emsp;");
					info_div.attr("class", "");
				}
				else {
					info_div.text(data.error);
					info_div.attr("class", "red-text text-darken-2");
				}
			}
		});

	});

	/* ########################## Resetting Form ##################### */

	input_form_fields_rssfeed = [
		'rssfeed_link',
		'rssfeed_title',
	]

	function clearFields_rssfeed(){
		for (field in input_form_fields_rssfeed){
			var input = $("#"+input_form_fields_rssfeed[field]);
			var label = input.siblings('label');

			var init_value = input.data('init');

			if (init_value == "" && label.hasClass( "active" )){
				label.removeClass("active");
				input.val("");
			}
			else if (init_value != "") {
				input.val(init_value);
				if (! label.hasClass( "active" ))
					label.addClass("active");
			}
		}
		$("#link-ajax-rslt").html("&emsp;");
		$("#link-ajax-rslt").attr("class", "");
	}

	$("#reset-btn-rssfeed").click(function() {
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
			clearFields_rssfeed();
			swal.close();
		});
	});

	/* ########################## Saving Form ##################### */

	function get_fields_rssfeed(){
		var rslt = {};
		for (field in input_form_fields_rssfeed){
			//console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
			var input = $("#"+input_form_fields_rssfeed[field]);
			rslt[input_form_fields_rssfeed[field]] = input.val();
		}
		return rslt;
	}

	$("#save-btn-rssfeed").click(function() {

		var feed_id = $("#rssfeed_id").val();

		if (feed_id == "-1"){
			var api_url = "/api/1.0/authenticated/post/rssfeed/";
			var request_type = "POST";
			var await_text = "Verifying and subscribing to the RSS Feed ...";
			var success_text = "RSS Feed Added with success!";
		}
		else {
			var api_url = "/api/1.0/authenticated/modify/rssfeed/"+feed_id+"/";
			var request_type = "PUT";
			var await_text = "Verifying and modifying the RSS Feed ...";
			var success_text = "RSS Feed Modified with success!";
		}

		var csrftoken = Cookies.get('csrftoken');
		var info_div = $("#link-ajax-rslt");

		if (! isUrlValid($("#rssfeed_link").val()) ){ // URL empty or not valid
			info_div.text("Link is empty or not Valid");
			info_div.attr("class", "red-text text-darken-2");
			return false;
		}

		if ( $("#rssfeed_title").val() == "" ){ // Title empty
			info_div.text("Title is empty");
			info_div.attr("class", "red-text text-darken-2");
			return false;
		}

		var feed_data = get_fields_rssfeed();

		$.ajax({
			url : api_url,
			type : request_type,
			data: feed_data,
			timeout: 5000, // sets timeout to 5 seconds
			dataType : "json",
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
				info_div.text(await_text);
				info_div.attr("class", "green-text text-darken-2");
			},
			error: function(jqXHR, textStatus){
				if(textStatus === 'timeout')
				{
					info_div.text("Request Timeout, please try again...");
					info_div.attr("class", "red-text text-darken-2");
				}
			},
			success: function(data){
				if (data.success) {
					swal({
						title: "Good job!",
						text: success_text,
						type: "success",
						timer: 1500,
						showConfirmButton: false,
						cache: false,
					}, function(){
						$("#close-btn-rssfeed").trigger( "click" );
						if (feed_id != "-1"){

							row = $('#feed-id-' + feed_id);
							edit_btn = $('#edit-btn-id-' + feed_id);
							// Edit Title
							var title = feed_data['rssfeed_title'];
							$(row.children()[1]).text(title);
							edit_btn.data("title", title);

							// Edit Domain
							var domain = feed_data['rssfeed_link'].split('//')[1].split('/')[0];
							$(row.children()[2]).text(domain);

							// Edit Link
							var link = feed_data['rssfeed_link'];
							$(row.children()[3]).text(link);
							edit_btn.data("link", link);
						}
						/*
						else {
							var id = data.RSSFeedID;
							var title = feed_data['rssfeed_title'];
							var link = feed_data['rssfeed_link'];
							var domain = link.split('//')[1].split('/')[0];

							table.row.add( [
								'<td>'+id+'</td>',
								'<td>'+title+'</td>',
								'<td>'+domain+'</span>',
								'<td>'+link+'</td>',
								'<td>0</td>',
								'<td><a id="edit-btn-id-'+id+'" class="modal-trigger edit-rssfeed-btn"  data-id="'+id+'" data-title="'+title+'" data-link="'+link+'" href="#modal-rss-feed">Edit</a></td>',
								'<td><a class="delete-feed" data-id="'+id+'" href="#">Delete</a></td>',
							] ).draw();
						}
						*/
						swal.close();
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
					}, function(){
						info_div.html("&emsp;");
						info_div.attr("class", "");
					});
				}
			}
		});
	});

});
