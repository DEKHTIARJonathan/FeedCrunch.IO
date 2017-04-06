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
    var switches_list = [
        'link-visible',
        'twitter',
        'facebook',
        'linkedin',
        'gplus',
        'auto-format'
    ]

    function clearFields(){

        var title = $("#title").data("init");
        var link = $("#link").data("init");

        $("#tags").materialtags('removeAll');

        if (title == "" || link == "") { // Creating a new article
            $("#title").val('').removeClass("valid").siblings().removeClass("active");
            $("#link").val('').removeClass("valid").siblings().removeClass("active");
        }

        else{ // Modifying an article
            $("#title").val(title);
            $("#link").val(link);
            $("#tags").materialtags('add', $("#tags").data( "init"));
        }

        for (switch_box in switches_list){
            var input = $("#"+switches_list[switch_box]);

            if (!input.is(':disabled')){
                var init_val = input.data("init").toLowerCase() == "true"; // Transforming "string to boolean"
                input.prop('checked', init_val);
            }
        }
    }

    clearFields(); // Required to display correctly the switches

    var request_url = window.location.pathname;

    if (request_url.indexOf("article/add") != -1){  // Add Form
        var api_url = "/api/1.0/authenticated/post/article/";
        var query_type = "POST";
    }
    else{
        var article_id = request_url.split("/", 6)[5];
        var api_url = "/api/1.0/authenticated/modify/article/"+article_id+"/";
        var query_type = "PUT";
    }

    $("#submit").click(function() {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
          url : api_url,
          type : query_type,
          contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
          dataType : "json",
          data: {
            title: $("#title").val(),
            link: $("#link").val(),
            tags: $("#tags").val(),
            activated: $('#link-visible').prop('checked'),
            twitter: $('#twitter').prop('checked'),
            facebook: $('#facebook').prop('checked'),
            linkedin: $('#linkedin').prop('checked'),
            gplus: $('#gplus').prop('checked'),
            autoformat: $('#auto-format').prop('checked'),
          },
          beforeSend: function(xhr) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          },
          success: function(data){
              if (data.success) {
                  if (data.operation == "submit article"){
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
                          title: "Article Modified!",
                          text: "Redirecting you to the edit listing in 3 seconds.",
                          type: "success",
                          timer: 3000,
                          showConfirmButton: false,
                      }, function(){
                          window.location = request_url.split("/", 5).join("/")+"/"
                          swal.close();
                      });
                  }

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
            swal.close();
        });
    });



});
