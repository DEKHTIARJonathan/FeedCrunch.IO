$( document ).ready(function() {

    var form = $("#example-form");
    var validator = $("#example-form").validate({
        errorPlacement: function errorPlacement(error, element) { element.after(error); },
    });

	var birthdate_input = $("#birthdate");

	var birthdate = birthdate_input.pickadate({
      format: 'dd/mm/yyyy',
	  closeOnSelect: true,
      selectMonths: true, // Creates a dropdown to control month
      selectYears: 50 // Creates a dropdown of 15 years to control year
  	});
  //

  	var picker = birthdate.pickadate('picker');
	picker.set('select', birthdate_input.data("init"), { format: 'dd/mm/yyyy' });

});
