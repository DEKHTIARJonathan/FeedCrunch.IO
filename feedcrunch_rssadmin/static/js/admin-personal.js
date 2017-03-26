$( document ).ready(function() {

    /*
    var form = $("#example-form");
    var validator = $("#example-form").validate({
        errorPlacement: function errorPlacement(error, element) { element.after(error); },
    });
    */

    $('#country').material_select(); // Select Initialization
    $("#gender").material_select(); // Select Initialization



    /* Calculating the maximum date */
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear() - 15;

    if(dd<10) {
        dd='0'+dd
    }

    if(mm<10) {
        mm='0'+mm
    }

    var max_birthdate = today = dd+'/'+mm+'/'+yyyy;


    var birthdate_input = $("#birthdate");
    var birthdate = birthdate_input.pickadate({
      format: 'dd/mm/yyyy',
      closeOnSelect: true,
      closeOnClear: true,
      selectMonths: true, // Creates a dropdown to control month
      selectYears: 50, // Creates a dropdown of 15 years to control year
      max: max_birthdate;
    });

      var picker = birthdate.pickadate('picker');
    var user_birthdate = birthdate_input.data("init");

    if (user_birthdate != "None")
        picker.set('select', user_birthdate, { format: 'dd/mm/yyyy' });

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
        "newsletter_subscribtion", // Not Saved yet !
    ]

    function clearFields(){
        for (field in form_fields){
            //console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
            var input = $("#"+form_fields[field]);
            input.val(input.data("init"));
        }
        $("#country").material_select();
        $("#gender").material_select();
    }

    function get_fields(){
        var rslt = {};
        for (field in form_fields){
            //console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
            var input = $("#"+form_fields[field]);
            rslt[form_fields[field]] = input.val();
        }
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
