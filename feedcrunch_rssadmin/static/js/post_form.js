ajaxURL = ""
if (window.location.pathname.slice(-4) == "add/"){
	ajaxURL = '../tags/json/'
}
else {
	ajaxURL = '../../tags/json/'
}

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

var tagApi = jQuery(".tm-input").typeahead(null, {
	name: 'tags',
	displayKey: 'name',
	source: tags.ttAdapter(),
	autoselect: true,
}).on('typeahead:autocompleted', function (e, datum) {
	console.log('selected');
	console.log(datum);
}).on('typeahead:selected', function (e, d) {
	tagApi.tagsManager("pushTag", d.name);
	tagApi.typeahead('close');
	tagApi.typeahead("val", '');
	tagApi.typeahead('setQuery', '');
}).bind('typeahead:render', function(e) {
	$('#tagInputField').parent().find('.tt-selectable:first').addClass('tt-cursor');
});

prefilled_data = $("#tagInputField").data("init");
if (prefilled_data == "")
	prefilled_data = null;

tagApi.tagsManager({
	prefilled: prefilled_data,
	CapitalizeFirstLetterOnly: true,
	delimiters: [13, 32],
	maxTags: 5,
	maxTagsBehavior: 'disable',
	/*
	Default: [9,13,44] (tab, enter, comma). Delimiters should be numeric ASCII char codes.
	Please note the following:
		The following values are handled as key codes:
			9 (tab),
			13 (enter),
			16 (shift),
			17 (ctrl),
			18 (alt),
			19 (pause/break),
			32 (space)
			37 (leftarrow),
			38 (uparrow),
			39 (rightarrow),
			40 (downarrow)
	*/
	deleteTagsOnBackspace: false,
	hiddenTagListId: 'tagListField',
	hiddenTagListName: 'tagListField',
	tagsContainer: tagContainer,
	tagCloseIcon: '×',
	tagClass: '',
	validator: null,
	onlyTagList: false
}).on('keyup', this, function (event) {
	if (event.keyCode == 13) {
		if ($('#tagInputField').parent().find('.tt-selectable:first').length == 0){
			tagApi.tagsManager("pushTag", $('#tagInputField').val());
		}
	}
}).on('tm:hide', function(e, taglist) {
	tagApi.typeahead("val", '');
	tagApi.typeahead('setQuery', '');
});

$(function() {
	$("[class='switch-checkbox']").bootstrapSwitch();
});

$(document).ready(function(){
	$("[rel=tooltip]").tooltip({
		position: {
			my: "center bottom-20",
			at: "center top",
			using: function( position, feedback ) {
				$( this ).css( position );
				$( "<div>" )
					.addClass( "arrow" )
					.addClass( feedback.vertical )
					.addClass( feedback.horizontal )
					.appendTo( this );
			}
		}
	});
});
