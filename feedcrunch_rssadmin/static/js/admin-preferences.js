$( document ).ready(function() {

    var form_fields = [
        'visibility',
        'autoformat',
        'twitter',
        'facebook',
        'linkedin',
        'slack'
    ];

    function clearFields(){
        for (field in form_fields){
            var input = $("#"+form_fields[field]);
            if (!input.is(':disabled')){
                var init_val = input.data("init").toLowerCase() == "true"; // Transforming "string to boolean"
                input.prop('checked', init_val);
            }
        }
    }

    clearFields(); // Required to display correctly the switches

    $("#reset-btn").click(function() {
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

    function get_fields(){
        var rslt = {};
        for (field in form_fields){
            var input = $("#"+form_fields[field]);
            rslt[form_fields[field]] = input.prop('checked');
        }
        return rslt;
    }

    $("#save-btn").click(function() {
        var api_url = "/api/1.0/authenticated/modify/user/preferences/";
        var csrftoken = Cookies.get('csrftoken');

        $.ajax({
            url : api_url,
            type : "PUT",
            data: get_fields(),
            dataType : "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                if (data.success) {
                    swal({
                        title: "Good job!",
                        text: "Your preferences have been modified with success!",
                        type: "success",
                        timer: 1500,
                        showConfirmButton: false,
                        cache: false,
                    });
                }
                else {
                    swal({
                        title: "Something went wrong!",
                        text: data.error,
                        type: "error",
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "I'll retry later",
                        closeOnConfirm: true
                    });
                }
            }
        });
    });
});
