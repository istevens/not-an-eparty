$(function() {
    var name = $("#name"),
        email = $("#email"),
        allFields = $([]).add(name).add(email);

    $("#rsvp-dialog").dialog({
        bgiframe: true,
        autoOpen: false,
        draggable: false,
        width: 450,
        modal: true,
        buttons: {
            'RSVP': function() {
                var submitOptions = {
                    url: 'rsvp',
                    type: 'POST',
                    dataType: 'json',
                    data: $("#rsvpForm").serialize(),
                    success: function(html) {
                        $("#rsvp-dialog").dialog('close');
                        $("#rsvp").text('Thanks for RSVPing!');
                    },
                    error: function(req, st, ex) {
                        alert(req.responseText);
                    }
                };

                // Manually trigger validation
                if ($("#rsvpForm").validate().form() == true) {
                    $.ajax(submitOptions)
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
        errorPlacement: function(error, elem) {
            error.insertBefore(elem);
        },
        focusCleanup: true
    });

});
