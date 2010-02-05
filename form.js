$(function() {
    var name = $("#name"),
        email = $("#email"),
        allFields = $([]).add(name).add(email),
        tips = $("#validateTips");

    $("#rsvp-dialog").dialog({
        bgiframe: true,
        autoOpen: false,
        width: 450,
        modal: true,
        buttons: {
            'RSVP': function() {
                var submitOptions = {
                    url: 'rsvp',
                    type: 'POST',
                    dataType: 'json',
                };

                // Manually trigger validation
                if ($("#rsvpForm").validate().form() == true) {
                    $('#rsvpForm').ajaxSubmit(submitOptions);
                    allFields.removeClass('ui-state-error');
                }

            },
            Cancel: function() {
                $(this).dialog('close');
            }
        },
        close: function() {
            allFields.val('').removeClass('ui-state-error');
        }
    });

    $('#rsvp').click(function() {
        $('#rsvp-dialog').dialog('open');
    });

    $('#rsvpForm').validate({
        rules: {
            recaptcha_response_field: "required"
        },
        errorPlacement: function(error, elem) {
            if(elem.attr("id") == "recaptcha_response_field") {
                error.insertAfter($('#recaptcha_label'));
            } else {
                error.insertBefore(elem);
            }
        },
        focusCleanup: true
    });

});
