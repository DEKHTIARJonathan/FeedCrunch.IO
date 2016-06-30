function preg_quote( str ) {
	// http://kevin.vanzonneveld.net
	// +   original by: booeyOH
	// +   improved by: Ates Goral (http://magnetiq.com)
	// +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +   bugfixed by: Onno Marsman
	// *     example 1: preg_quote("$40");
	// *     returns 1: '\$40'
	// *     example 2: preg_quote("*RRRING* Hello?");
	// *     returns 2: '\*RRRING\* Hello\?'
	// *     example 3: preg_quote("\\.+*?[^]$(){}=!<>|:");
	// *     returns 3: '\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:'

	return (str+'').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1");
}

function highlight( data, search )
{
	return data.replace( new RegExp( "(" + preg_quote( search ) + ")" , 'gi' ), "<mark>$1</mark>" );
}

var request = null;

$('#search-bar').keyup(function(){

	var postForm = {
		'search_str' : $('#search-bar').val(),
		'csrfmiddlewaretoken' : $('input[name^=csrfmiddlewaretoken]').val()
	};

	//check for existing ajax request
	if (request != null){
		request.abort();
		request = null;
	}
	request = $.ajax({
		url: 'search/',
		type: 'POST',
		dataType: 'json',
		data: postForm,
		error: function() {
		  console.log("Request Aborted");
		},
		success: function(data) {
				var rslt = $.parseJSON(JSON.stringify(data));
				if (rslt.status === "OK"){
				$('#viewer_body').empty();

				var i;
				var posts = rslt.posts;
				for (i = 0; i < posts.length; ++i) {
					var str_search = rslt.search_str;
					var title = highlight(posts[i]["title"], str_search);
					var domain_name = highlight(posts[i]["domain_name"], str_search);
					var published_date = posts[i]["when"];
					var id = posts[i]["id"];


					var row = '\
					<tr>\
						<td style="vertical-align:middle;" class="hidden_column">'+id+'</td>\
						<td style="vertical-align:middle;">'+title+'<span class="domain_value"> ~ ('+domain_name+')</span></td>\
						<td style="vertical-align:middle;" class="hidden_column">'+published_date+'</td>\
						<td style="vertical-align:middle;"><a href="redirect.php?postID='+id+'" target="_blank">Link</a></td>\
					</tr>';
					$("#viewer tbody").append(row);
				}
				}
			else
				alert("Request Error");

	   }
	});
});
