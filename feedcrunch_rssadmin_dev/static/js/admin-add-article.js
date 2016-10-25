$( document ).ready(function() {
    var validator = $("#add-form").validate({
        debug: true
    });

    /* ################################################# TypeAhead ####################################################### */

    var ajaxURL = "/api/1.0/authenticated/get/tags/";
    var max_tags = 5;
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

    $("#tags").materialtags({
        maxTags                    : max_tags,
        trimValue                  : true,
        confirmKeys                : [9, 13, 32, 44, 188],
        deleteTagsOnBackspace      : false,
        deleteTagsOnDeleteKey      : false,
        MoveTagOnLeftArrow         : false,
        MoveTagOnRightArrow        : false,
        CapitalizeFirstLetterOnly  : true,
        typeaheadjs : [{
            autoselect  : true,
            highlight   : true,
        },
        {
            name        : 'tags',
            displayKey   : 'name',
            valueKey    : 'name',
            source      : tags.ttAdapter(),
        }]
    });

    /* ################################################# Sweet Alert ####################################################### */

    function clearFields(){
        $("#title").val('').removeClass("valid").siblings().removeClass("active");
        $("#link").val('').removeClass("valid").siblings().removeClass("active");
        $("#tags").materialtags('removeAll');
        $('#twitter').prop('checked', false);
        $('#auto-format').prop('checked', false);
        $('#link-visible').prop('checked', false);
    }

    $("#submit").click(function() {
        $.ajax({
    	  url : "/api/1.0/authenticated/post/article/",
    	  type : "POST",
    	  contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
    	  dataType : "json",
    	  data: {
    		title: $("#title").val(),
    		link: $("#link").val(),
    		tags: $("#tags").val(),
    		csrfmiddlewaretoken: $('input[name^=csrfmiddlewaretoken]').val(),
    		activated: $('#link-visible').prop('checked'),
    		twitter: $('#twitter').prop('checked'),
    		autoformat: $('#auto-format').prop('checked'),
    	  },
          success: function(data){
              if (data.success) {
                  clearFields();
                  swal({
                      title: "Good job!",
                      text: "Article Submitted!",
                      type: "success",
                      timer: 1500,
                      showConfirmButton: false,
                  });
      		}
            else{
                swal({
                    title: "Something went wrong!",
                    text: data.error,
                    type: "error",
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "I'll Fix it!",
                    closeOnConfirm: true
                });
            }
          }
        })
    });

    $("#reset").click(function() {
        swal({
            title: "Are you sure ?",
            text: "Do you really want to reset all the fields ?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, please reset!",
            cancelButtonText: "Please No!",
            closeOnConfirm: true,
            closeOnCancel: true
        }, function(){
            clearFields();
        });
    });



});
