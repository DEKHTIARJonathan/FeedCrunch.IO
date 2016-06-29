$(function() {
  $("#submit").click( function()
  {
    $.ajax({
      url : "ajax/",
      type : "POST",
      data: {title: $("#title").val(), link: $("#link").val(), csrfmiddlewaretoken: $('input[name^=csrfmiddlewaretoken]').val()},
      dataType : "html",

      success: function(data){
        if (data != 1) {
           $("#resultatUpload").attr('class', 'alert alert-warning show');
           $("#resultatUpload").html("Attention, cette action n'a pas pu être enregistrée.");
        }
        else
        {
          $("#resultatUpload").attr('class', 'alert alert-success show');
          $("#resultatUpload").html("Enregistrement effectué avec succès.");
          $("#title").val("");
          $("#link").val("")
        }
      }
    });
  });
});
