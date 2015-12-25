$(function() {
    var form = $("#teamForm");
    var status = $('#status');

    function errorHandeling(obj, error) {
        obj.parent().addClass("has-error");
        obj.after('<div class="help-block with-errors">' + error + '</div>');
        obj.siblings(".help-block").children(".errorlist").addClass("list-unstyled");
        obj.focus(function(event) {
            $(event.target).parent().removeClass("has-error");
            $(event.target).siblings(".help-block").slideUp( 900 );
            setTimeout(function(){
                $(event.target).siblings(".help-block").remove();
            }, 950);
        });
    }

    form.submit(function() {
        // submit the form
        $(this).ajaxSubmit({
            beforeSend: function() {
                $('#teamForm input').attr('readonly', 'readonly');
                $("#teamForm .btn").attr('disabled', 'disabled');
            },
            complete: function(xhr) {
                var respone_msg = $.parseJSON(xhr.responseText);
                status.html(respone_msg.msg);
                setTimeout(function(){
                    $("#status").empty();
                }, 2000);
                status.html(respone_msg.msg);
                $('#teamForm input').removeAttr( "readonly" );
                $("#teamForm .btn").removeAttr('disabled', 'disabled');
            },
            statusCode: {
            400: function( data ) {
                var errors_list = $.parseJSON(data.responseText);
                $.each( errors_list, function(k, v) {
                    // person form
                    if (!$('#id_' + k).parent().hasClass("has-error")){
                        errorHandeling($('#id_' + k), v)
                    }
                });
            }
        }
        });
        // return false to prevent normal browser submit and page navigation
        return false;
    });
});