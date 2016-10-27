$(document).ready(function() {
	var table = $('#post-listing').DataTable({
		"columns": [
			{ "searchable": false},
			null,
			null,
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
	} );

	$("#article-searchbar").on('input',function(e){
		table.search( $(this).val() ).draw();
	});

	function responsive_columns () {
		width = $( window ).width();

		if (width < 1200) {
			table.column( 0 ).visible( false ); // hide ID
			table.column( 2 ).visible( false ); // hide when
			table.column( 3 ).visible( false ); // hide domain
		}
		else if (width < 1500) {
			table.column( 0 ).visible( false ); // hide ID
			table.column( 2 ).visible( true ); // hide domain
			table.column( 3 ).visible( false ); // hide when
		}
		else {
			table.column( 0 ).visible( true ); // hide ID
			table.column( 2 ).visible( true ); // hide domain
			table.column( 3 ).visible( true ); // hide when
		}
		table.responsive.rebuild();
		table.responsive.recalc();
	};

	responsive_columns ();

	$( window ).resize(function() {
		responsive_columns ();
	});



	$('.dataTables_length select').addClass('browser-default');
});
