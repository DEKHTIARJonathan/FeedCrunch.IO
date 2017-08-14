$( document ).ready(function() {
    //jQuery time
    var current_fs, next_fs, previous_fs; //fieldsets
    var left, opacity, scale; //fieldset properties which we will animate
    var animating; //flag to prevent quick multi-click glitches

    $(".next").click(function(){
        if(animating) return false;
        animating = true;

        current_fs = $(this).parent().parent();
        next_fs = $(this).parent().parent().next();

        //activate next step on progressbar using the index of next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50)+"%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({'transform': 'scale('+scale+')'});
                next_fs.css({'left': left, 'opacity': opacity});
            },
            duration: 800,
            complete: function(){
                current_fs.hide();
                animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    });

    $(".submit").click(function(){
        return false;
    });

    var interests_required_number = 3;

    $('.interest-checkbox').on('change', function(evt) {

        var amount_checked = $('.interest-checkbox:checked').length;

        if(amount_checked > interests_required_number) {
            this.checked = false;
        }
        else if (amount_checked == interests_required_number) {
            $("#interests-btn").prop("disabled", false);
            $("#interests-btn").html("Next Step");
        }
        else{
            $("#interests-btn").prop("disabled", true);
            $("#interests-btn").html("Select 3 Interests to Continue ...");
        }
    });

    // =================================================================== FORM SUBMITTING ===========================================================
    $('#country').material_select(); // Select Initialization
    $("#gender").material_select(); // Select Initialization

    var birthdate_input = $("#birthdate");

    var birthdate = birthdate_input.pickadate({
        format: 'dd/mm/yyyy',
        closeOnSelect: true,
        closeOnClear: true,
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 50, // Creates a dropdown of 15 years to control year
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
    ]

    function clearFields(){
        for (field in form_fields){
            //console.log(social_networks[field]+ " = " +$("#"+social_networks[field]).val());
            var input = $("#"+form_fields[field]);
            var data = input.data("init");

            if (data != ""){
                $("label[for='" + form_fields[field] + "']").addClass("active");
                console.log(form_fields[field]);
            }

            input.val(data);
        }

        $("#country").material_select();
        $("#gender").material_select();
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

    $("#save-btn").click( function(event) {
        for (i = 0; i < interests_required_number; i++) {
            $('input#interest'+(i+1)).val($("#"+$('.interest-checkbox:checked')[i].id).data("name"));
        }

        $("#onboarding_form").submit();
    });
    /*
	$('.interest-checkbox').on('change', function(evt) {
		var limit = 3;
		var amount_checked = $('.interest-checkbox:checked').length;
		if(amount_checked > limit) {
			this.checked = false;
		}
		else if (amount_checked == limit) {
			$(".continue").prop("disabled", false);
			$(".continue").html("Continue &rarr;");
		}
		else{
			$(".continue").prop("disabled", true);
			$(".continue").html("Select 3 to Continue");
		}
	});
    */
});
