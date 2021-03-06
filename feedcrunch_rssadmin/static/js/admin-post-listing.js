$(document).ready(function() {
    var table = $('#post-listing').DataTable({
        "columns": [
			{ "width": "35px", "searchable": false},  // ID
			{ "width": "auto", "searchable": true},  // TITLE
			{ "width": "240px", "searchable": true},  // DOMAIN
			{ "width": "75px", "searchable": false},  // DATE
			{ "width": "30px", "searchable": false}, // LINK
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


	function reset_click_delete(){
		$(".delete-link").off("click");
		$(".delete-link").click( function(){
	        // $("#test").parent().parent().remove()
	        var current_row = $(this);
	        var post_id = $(this).data("id");

	        var api_url = "/api/1.0/authenticated/delete/article/"+post_id+"/";
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
		                        text: "Article deleted with success!",
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


});
