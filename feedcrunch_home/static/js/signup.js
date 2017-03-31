jQuery(function($) {
    $.validator.addMethod("regex", function(value, element, regexpr) {
        return regexpr.test(value);
    }, "Not Valid");

    $("[name='registration']").validate({
        rules: {
            username: {
                required: true,
                minlength: 4,
                remote: {
                    url: "/api/1.0/public/post/validate/username/",
                    type: "post",
                    data: {
                        username: function() {
                            return $("#username").val();
                        },
                    },
                    dataType: 'json',
                    dataFilter: function(data) {
                        data = JSON.parse(data);

                        if (data.success && data.available) {
                            return true;
                        } else {
                            return false;
                        }
                    },
                    complete: function(xhr) {}
                }
            },
            firstname: {
                required: true,
                minlength: 2
            },
            lastname: {
                required: true,
                minlength: 2
            },
            birthdate: {
                required: true,
                regex: /([0-2]\d{1}|3[0-1])\/(0\d|1[0-2])\/(19|20)\d{2}$/,
            },
            gender: {
                required: true,
            },
            country: {
                required: true,
            },
            email: {
                required: true,
                regex: /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.([a-z]{2,4})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i
            },
            password: {
                required: true,
                regex: /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z\d]{8,}/,
            },
            password_again: {
                equalTo: "#password"
            }
        },
        messages: {
            password: {
                required: "Enter a password",
                regex: "Please enter at least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9"
            },
            email: {
                required: "Enter an email",
                regex: "Enter a valid email"
            },
            password_again: {
                equalTo: "The Passwords are not identical"
            },
            birthdate: {
                required: "Enter a birthdate",
                regex: "Enter a valid birthdate format (dd/mm/yyyy)"
            },
            username: {
                remote: "Username already taken ..."
            }
        },
        /*
        // Specify validation error messages
        messages: {
            firstname: "Please enter your firstname",
            lastname: "Please enter your lastname",
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 8 characters long"
            },
            email: "Please enter at least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9"
        },
        */
        errorPlacement: function(error, element) {
                var placement = $(element).data('error');
                if (placement) {
                    $(placement).append(error)
                } else {
                    error.insertAfter(element);
                }
            }
            /*
            submitHandler: function(form) {
                form.submit();
            }
            */
    });
});
