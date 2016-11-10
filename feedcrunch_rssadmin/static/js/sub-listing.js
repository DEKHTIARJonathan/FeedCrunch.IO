$(document).ready(function() {
    var table = $('#sub-listing').DataTable({
        "columns": [
            { "searchable": false},
            null,
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

		// reset_click_delete();
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
        }
        else if (width < 1500) {
            table.column( 0 ).visible( false ); // hide ID
            table.column( 2 ).visible( true ); // show domain
            table.column( 3 ).visible( false ); // hide link
        }
        else {
            table.column( 0 ).visible( true ); // show ID
            table.column( 2 ).visible( true ); // show domain
            table.column( 3 ).visible( true ); // show link
        }
        table.responsive.rebuild();
        table.responsive.recalc();
    };

    responsive_columns ();

    $( window ).resize(function() {
        responsive_columns ();
    });

    $('.dataTables_length select').addClass('browser-default');

	/*
	function reset_click_delete(){
		$(".delete-link").off("click");
		$(".delete-link").click( function(){
	        // $("#test").parent().parent().remove()
	        var current_row = $(this);
	        var post_id = $(this).data("id");

	        var api_url = "/api/1.0/authenticated/delete/article/"+post_id+"/";
	        var csrftoken = Cookies.get('csrftoken');

	        $.ajax({
	            url : api_url,
	            type : "DELETE",
	            data: {
	                postID: post_id,
	            },
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
	    });
	}

	reset_click_delete();

	*/


});
