$(document).ready(function() {

	var table = $('#recommendation-listing').DataTable({
		"columns": [
			{ "width": "auto", "searchable": true},   // TITLE
			{ "width": "190px", "searchable": true},  // FEED
			{ "width": "170px", "searchable": true},  // DOMAIN
			{ "width": "55px", "searchable": false},  // HOTNESS
			{ "width": "125px", "searchable": false}, // PUBLISH
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

		//reset_click_delete();
		//reset_click_edit();
	} );

	$("#article-searchbar").on('input',function(e){
		table.search( $(this).val() ).draw();
	});

	function responsive_columns () {
		width = $( window ).width();

		if (width < 1200) {
			table.column( 1 ).visible( false ); // hide feed
			table.column( 2 ).visible( false ); // hide domain
		}
		else if (width < 1500) {
			table.column( 1 ).visible( false ); // hide feed
			table.column( 2 ).visible( true ); // hide domain
		}
		else {
			table.column( 1 ).visible( true ); // hide feed
			table.column( 2 ).visible( true ); // hide domain
		}
		table.responsive.rebuild();
		table.responsive.recalc();
	};

	responsive_columns ();

	$( window ).resize(function() {
		responsive_columns ();
	});

	$('.dataTables_length select').addClass('browser-default');

	// ================================================================ Button Mark All As Read ===================================================
	$("#mark-all-as-read-btn").click( function(){
		var RSSArticles_Listing = "";
		$('#recommendation-listing > tbody  > tr').each(function() {
			RSSArticles_Listing += $(this).attr('id').substring(7) + ",";
		});

		var api_url = "/api/1.0/authenticated/mark_list_as_read/rssarticle/";
		var query_type = "PUT";

		var csrftoken = Cookies.get('csrftoken');


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
			$.ajax({
				url : api_url,
				type : query_type,
				dataType : "json",
				data: {
					'listing': RSSArticles_Listing,
				},
				beforeSend: function(xhr) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				},
				success: function(data){
					if (data.success) {
						location.reload();
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
		});

	});
	// ================================================================ Button Listing Actions =====================================================

	$(".delete-btn").click( function(){
		var current_row = $(this);
		var rssarticle_id = current_row.data("id");
		//table.row( current_row.parents('tr') ).remove().draw();

		var api_url = "/api/1.0/authenticated/mark_as_read/rssarticle/"+rssarticle_id+"/";
		var query_type = "PUT";

		var csrftoken = Cookies.get('csrftoken');

		$.ajax({
			url : api_url,
			type : query_type,
			contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
			dataType : "json",
			data: {},
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(data){
				if (data.success) {
					table.row( current_row.parents('tr') ).remove().draw();
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
	});

	$(".share-btn").click( function(){
		var btn = $(this);
		var title = btn.data("title");
		var link = btn.data("link");
		var id = btn.data("id");

		var field_title = $("#post-title");
		var label_title = field_title.siblings('label');

		var field_link = $("#post-link");
		var label_link = field_link.siblings('label');

		$("#post-tags").materialtags('removeAll');

		$("#post-id").val(id);


		field_title.val(title);
		field_title.data("init", title);

		if (! label_title.hasClass( "active" ))
			label_title.addClass("active");


		field_link.val(link);
		field_link.data("init", link);

		if (! label_link.hasClass( "active" ))
			label_link.addClass("active");

		$("#open-new-tab-btn-post").attr("href", "redirect/"+id+"/");

	});

	// ================================================================ Post Article Modal ========================================================

	// ######################################## TypeAhead #####################################

	var tagsURL = "/api/1.0/authenticated/get/tags/";
	var max_tags = 5;
	var max_suggestion_display = 5;

	var tags = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: max_suggestion_display,
		prefetch: {
			url: tagsURL,
			filter: function (list) {
				return $.map(list.tags, function (tag) { return { name: tag }; });
			},
			cache: false //NEW!
		}
	});

	tags.initialize();

	$("#post-tags").materialtags({
		maxTags					: max_tags,
		trimValue					: true,
		confirmKeys				: [9, 13, 32, 44, 188],
		deleteTagsOnBackspace		: false,
		deleteTagsOnDeleteKey		: false,
		MoveTagOnLeftArrow		 : false,
		MoveTagOnRightArrow		: false,
		CapitalizeFirstLetterOnly	: true,
		typeaheadjs : [{
			autoselect	: true,
			highlight	 : true,
		},
		{
			name		: 'tags',
			displayKey	 : 'name',
			valueKey	: 'name',
			source		: tags.ttAdapter(),
		}]
	});

	// ######################################## Resetting Form ################################

	function clearFields(){

		var field_title = $("#post-title");
		var label_title = field_title.siblings('label');
		var init_title = field_title.data("init");

		var field_link = $("#post-link");
		var label_link = field_link.siblings('label');
		var init_link = field_link.data("init");

		field_title.val(init_title);

		if (! label_title.hasClass( "active" ))
			label_title.addClass("active");


		field_link.val(init_link);

		if (! label_link.hasClass( "active" ))
			label_link.addClass("active");

		$("#post-tags").materialtags('removeAll');

		$('#post-link-visible').prop('checked', true);
		$('#post-twitter').prop('checked', false);
		$('#post-auto-format').prop('checked', false);

	}

	$("#reset-btn-post").click(function() {
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
			clearFields();
			swal.close();
		});
	});

	// #################################################### Submitting Form #################################


	var api_url = "/api/1.0/authenticated/post/article/";
	var query_type = "POST";

	$("#save-btn-post").click(function() {
		var csrftoken = Cookies.get('csrftoken');

		var article_id = $('#post-id').val();

		$.ajax({
			url : api_url,
			type : query_type,
			contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
			dataType : "json",
			data: {
				article_id: article_id,
				title: $("#post-title").val(),
				link:	$("#post-link").val(),
				tags: $("#post-tags").val(),
				activated: $('#post-link-visible').prop('checked'),
				twitter: $('#post-twitter').prop('checked'),
				autoformat: $('#post-auto-format').prop('checked'),
			},
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function(data){
				if (data.success) {
					swal({
						title: "Good job!",
						text: "Article Submitted!",
						type: "success",
						timer: 1500,
						showConfirmButton: false,
					},function(){
						$("#close-btn-post").trigger( "click" );
						table.row( $("#row-id-"+article_id)).remove().draw();
						swal.close();
					});
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
	});

});
