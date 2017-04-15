$( document ).ready(function() {

    /* ################################################# Sweet Alert ####################################################### */
    /*
    var switches_list = [
        'link-visible',
        'twitter',
        'facebook',
        'linkedin',
        'slack',
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

    */

    function getData(){
        var submission_dict = {};// create an empty array

        $(".slack-team-switch").each(function( index ) {
            team_name = $(this).closest('.slack-team').find(".slack-team-name").text();

            if (!(team_name in submission_dict)){ // Test if the key already exist in the dict
                submission_dict[team_name] = "";
            }

            channel_name = $(this).closest('.collection-item').find(".slack-channel-name").text();

            if ($( this ).prop('checked')){
                if (submission_dict[team_name] == "") {
                    submission_dict[team_name] = channel_name;
                } else {
                    submission_dict[team_name] = submission_dict[team_name] + "," + channel_name;
                }
            }
        });

        return submission_dict;

    }

    function clearFields(){
        $(".slack-team-switch").each(function( index ) {
            $(this).prop('checked', $(this).data("init"));
        });
    }

    clearFields(); // Required to display correctly the switches

    $(".unlink-slack-team-btn").click(function (e) {
        swal({
            title: "Are you sure ?",
            text: "Do you really want to delete this team from your account ?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, please remove!",
            cancelButtonText: "Please No!",
            closeOnConfirm: true,
            closeOnCancel: true
        }, function(){
            //clearFields();
            console.log("Reset Team Done");
            swal.close();
        });
        return false;
    });

    $("#submit").click(function() {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            url : "/api/1.0/authenticated/modify/user/social-networks/slack/",
            type : "PUT",
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            dataType : "json",
            data: getData(),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                if (data.success) {
                    swal({
                        title: "Modification Submited",
                        text: "You have successfully modified your Slack Posting Settings",
                        type: "success",
                        timer: 2000,
                        showConfirmButton: false,
                    }, function(){
                        swal.close();
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
            swal.close();
        });
    });

});
