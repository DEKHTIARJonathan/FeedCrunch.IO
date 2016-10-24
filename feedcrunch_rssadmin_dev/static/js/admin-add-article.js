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

	var citynames_json = [
	 {
		"value": 1,
		"text": "Amsterdam",
		"continent": "Europe"
	 },
	 {
		"value": 2,
		"text": "London",
		"continent": "Europe"
	 },
	 {
		"value": 3,
		"text": "Paris",
		"continent": "Europe"
	 },
	 {
		"value": 4,
		"text": "Washington",
		"continent": "America"
	 },
	 {
		"value": 5,
		"text": "Mexico City",
		"continent": "America"
	 },
	 {
		"value": 6,
		"text": "Buenos Aires",
		"continent": "America"
	 },
	 {
		"value": 7,
		"text": "Sydney",
		"continent": "Australia"
	 },
	 {
		"value": 8,
		"text": "Wellington",
		"continent": "Australia"
	 },
	 {
		"value": 9,
		"text": "Canberra",
		"continent": "Australia"
	 },
	 {
		"value": 10,
		"text": "Beijing",
		"continent": "Asia"
	 },
	 {
		"value": 11,
		"text": "New Delhi",
		"continent": "Asia"
	 },
	 {
		"value": 12,
		"text": "Kathmandu",
		"continent": "Asia"
	 },
	 {
		"value": 13,
		"text": "Cairo",
		"continent": "Africa"
	 },
	 {
		"value": 14,
		"text": "Cape Town",
		"continent": "Africa"
	 },
	 {
		"value": 15,
		"text": "Kinshasa",
		"continent": "Africa"
	 }
	]

/*
	var cities = new Bloodhound({
		datumTokenizer : Bloodhound.tokenizers.obj.whitespace('text'),
		queryTokenizer : Bloodhound.tokenizers.whitespace,
		local: citynames_json
	});
	cities.initialize();
*/
	var ajaxURL = "http://localhost:5000/@dataradar/admin/tags/json/";

	var tags = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: 10,
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

		if(code==32||code==13)
			tag = $(this).val();

		else if (code==188)
			tag = $(this).val().slice(0, -1); // We remove the comma

		if (tag != "") {
			e.preventDefault();
			input_typeahead.materialtags('add', { name: tag });
			$(this).val("");
			var tag_count = input_typeahead.materialtags('items').length;
			if (tag_count == max_tags){
				input_typeahead.materialtags('input').prop('readOnly', true);
				input_typeahead.prop('readOnly', true);
				$(this).blur();
			}
		}

	});

	input_typeahead.on('itemRemoved', function(event) {
		input_typeahead.materialtags('input').prop('readOnly', false);
		input_typeahead.prop('readOnly', false);
	});

});
