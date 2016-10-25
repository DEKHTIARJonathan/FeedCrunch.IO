$( document ).ready(function() {
	var validator = $("#add-form").validate({
		debug: true
	});


	$("#submit").click(function() {
		swal({
			title: "Good job!",
			text: "Article Submitted!",
			type: "success",
			timer: 1500,
			showConfirmButton: false,
		});
	});

	$("#reset").click(function() {
		swal({
			title: "Are you sure?",
			text: "You will not be able to recover this imaginary file!",
			type: "warning",
			showCancelButton: true,
			confirmButtonColor: "#DD6B55",
			confirmButtonText: "Yes, delete it!",
			closeOnConfirm: false
		},
		function(){
			swal("Deleted!", "Your imaginary file has been deleted.", "success");
		});
	});

	var ajaxURL = "http://localhost:5000/@dataradar/admin/tags/json/";
	var max_suggestion_display = 5;

	var tags = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: max_suggestion_display,
		prefetch: {
			url: ajaxURL,
			filter: function (list) {
				return $.map(list.tags, function (tag) { return { name: tag }; });
			},
			cache: false //NEW!
		}
	});

	tags.initialize();

	var input_typeahead = $("#example-typeahead");
	var max_tags = 2;

	input_typeahead.materialtags({
		itemValue	: 'name',
		itemText	: 'name',
		maxTags: max_tags,
		maxTagsBehavior: 'disable',
		typeaheadjs : {
			name: 'tags',
				displayKey: 'name',
				source: tags.ttAdapter(),
				autoselect: true,
		}
	});

	input_typeahead.materialtags('input').blur(function() {
		 $(this).val("");
	}).keyup(function(e){
		/*
		************ Keycodes ************
		Space = 32
		Enter = 13
		Comma = 188
		************ Keycodes ************
		*/
		var code = e.which; // recommended to use e.which, it's normalized across browsers
		var tag = "";

		if(code==32||code==13||code==188){
			e.preventDefault();
			tag = $(this).val();
			$(this).val("");
			tag = tag.split(',')[0] // we remove any existing comma
			tag = tag.split(' ')[0] // we stop after any space
			tag.trim();
			input_typeahead.materialtags('add', { name: tag });
		}
	});

	input_typeahead.on('itemAdded', function(event) {
		var tag_count = $(this).materialtags('items').length;
		if (tag_count == max_tags){
			input_typeahead.materialtags('input').prop('readOnly', true);
			input_typeahead.prop('readOnly', true);
			$(this).blur();
			input_typeahead.siblings().first().next().addClass( "looks-inactive" );
		}
	}).on('itemRemoved', function(event) {
		input_typeahead.materialtags('input').prop('readOnly', false);
		input_typeahead.prop('readOnly', false);
		input_typeahead.siblings().first().next().removeClass( "looks-inactive" );
	});

});
