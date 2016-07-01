$(function() {
  $("#submit").click( function(){
    $.ajax({
      url : "ajax/",
      type : "POST",
      data: {
        title: $("#title").val(),
        link: $("#link").val(),
        csrfmiddlewaretoken: $('input[name^=csrfmiddlewaretoken]').val(),
        activated: $("#activated_radio").bootstrapSwitch('state'),
        twitter: $("#twitter_radio").bootstrapSwitch('state'),
        autoformat: $("#auto_format").bootstrapSwitch('state')
      },
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
          $("#link").val("");
          $("#activated_radio").bootstrapSwitch('state', true);
          $("#twitter_radio").bootstrapSwitch('state', true);
          $("#auto_format").bootstrapSwitch('state', true);

        }
      }
    });
  });
});

$(function() {
  $("#clear").click( function(){
    $("#title").val("");
    $("#link").val("");
    $("#activated_radio").bootstrapSwitch('state', true);
    $("#twitter_radio").bootstrapSwitch('state', true);
    $("#auto_format").bootstrapSwitch('state', true);
  });
});
