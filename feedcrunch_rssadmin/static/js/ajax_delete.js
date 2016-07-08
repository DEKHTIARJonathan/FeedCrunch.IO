$(function() {
  $("#submit").click( function(){

  });
});

$(function() {
  $(".delete-link").click( function(){
	// $("#test").parent().parent().remove()
	var current_row = $(this);
	var post_id = $(this).data("id");

	$.ajax({
	  url : "ajax/",
	  type : "POST",
	  data: {
		postID: post_id,
		csrfmiddlewaretoken: $('input[name^=csrfmiddlewaretoken]').val(),
	  },
	  dataType : "json",

	  success: function(data){
		if (data.status == "success") {
		  current_row.parent().parent().remove();
		}
		else{
		  alert(data.error);
		}
	  }
	});

  });
});
