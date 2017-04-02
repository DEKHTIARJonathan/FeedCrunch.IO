$( document ).ready(function() {


    $('#country').material_select(); // Select Initialization
    $("#gender").material_select(); // Select Initialization

    /* Calculating the maximum date */
    var today = new Date();
    var max_yyyy = today.getFullYear() - 15;

    var birthdate_input = $("#birthdate");
    var birthdate_label = $("#birthdate-label");

    var birthdate = birthdate_input.pickadate({
        format: 'dd/mm/yyyy',
        closeOnSelect: true,
        closeOnClear: true,
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 50, // Creates a dropdown of 15 years to control year
        max: new Date(max_yyyy,0,1),
        onSet: function( arg ){
            if ( 'select' in arg ){ //prevent closing on selecting month/year
                this.close();
            }
        },
        onStart: function() {
            this.set('select', [1990, 0, 1]);
        }
    });

    var picker = birthdate.pickadate('picker');
    var user_birthdate = birthdate_input.data("init");

    birthdate_input.change(function() {
        if (birthdate_input.val() == "")
            birthdate_label.removeClass("active");
        else{
            birthdate_input.val(birthdate_input.val().trim());
            birthdate_label.addClass("active");
        }
    });

    if (! (typeof user_birthdate === "undefined")){
        picker.set('select', user_birthdate, { format: 'dd/mm/yyyy' });
    }

    form_fields = [
        'firstname',
        'lastname',
        'email',
        'birthdate',
        'country', // Select
        'gender', // Select
        'feedtitle',
        'description', // TextArea
        'job',
        'company_name',
        'company_website',
        "newsletter_subscribtion"
    ]

    function clearFields(){
        for (field in form_fields){
            //console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
            var input = $("#"+form_fields[field]);
            input.val(input.data("init"));
        }

        $("#newsletter_subscribtion").prop('checked', $("#newsletter_subscribtion").data("init").toLowerCase() == "true");

        $("#country").material_select();
        $("#gender").material_select();
    }

    clearFields(); // Required to display correctly the switches

    function get_fields(){
        var rslt = {};
        for (field in form_fields){
            //console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
            var input = $("#"+form_fields[field]);
            rslt[form_fields[field]] = input.val();
        }
        rslt["newsletter_subscribtion"] =  $("#newsletter_subscribtion").prop('checked');

        return rslt;
    }

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

    $("#save-btn").click(function() {
        var api_url = "/api/1.0/authenticated/modify/user/personal-info/";
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
                        text: "Personal Information modified with success!",
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
