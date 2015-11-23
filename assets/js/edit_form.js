$(function() {
    var form = $("#commonform");

    var bar = $('.progress-bar');
    var percent = $('.percent');
    var status = $('#status');

    $( ".bootstrap-filestyle" ).css({"z-index": "1"});

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
                status.empty();
                $('#commonform input, #commonform textarea').attr('readonly', 'readonly');
                $("#commonform .btn").attr('disabled', 'disabled');
                var percentVal = '0%';
                bar.addClass( "active" );
                bar.width(percentVal);
                percent.html(percentVal);
            },
            uploadProgress: function(event, position, total, percentComplete) {
                var percentVal = percentComplete + '%';
                bar.width(percentVal);
                percent.html(percentVal);
            },
            complete: function(xhr) {
                bar.removeClass( "active" );
                var respone_msg = $.parseJSON(xhr.responseText);
                status.html(respone_msg.msg);
                $('#commonform input, #commonform textarea').removeAttr( "readonly" );
                $("#commonform .btn").removeAttr('disabled', 'disabled');
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