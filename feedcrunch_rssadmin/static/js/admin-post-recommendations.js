$(document).ready(function() {

	var table = $('#recommendation-listing').DataTable({
		"columns": [
			{ "searchable": true},
			{ "searchable": true},
			{ "searchable": true},
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

	// ================================================================ OPML MODAL ========================================================

	$(".delete-btn").click( function(){
		var current_row = $(this);
		table.row( current_row.parents('tr') ).remove().draw();
	});

	$(".share-btn").click( function(){
		/*
		swal({
			title: "Good job!",
			text: "Article featured in your feed!",
			type: "success",
			timer: 1500,
			showConfirmButton: false,
			cache: false,
		});
		*/
		console.log();
	});

});
