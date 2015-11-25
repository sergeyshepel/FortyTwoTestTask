String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

$( function() {
  setInterval( function() {
    var latest_id = $( ".table tbody>tr>td:first-child" ).html();

    $.getJSON( "/requests/", { "latest_id": latest_id.toString() }, function( data ) {
        var default_title = $( "title" ).text();
        var new_requests = jQuery.parseJSON( data.requests );
        var actual_number_of_requests = Object.keys(new_requests).length;

        function unset_title( title ) {
            $( "title" ).text( title );
        };

        function prepend_new_requests(response_data, requests_in_response, total_number_of_new_requests){
            $( "title" ).text('(' + total_number_of_new_requests + ')' + " new requests stored in db!");

            $.each(response_data, function( index, item ){
                var isoDate  = new Date(item.fields.time).toUTCString().replace("GMT", "");
                tr = '<tr><td hidden>'+ item.pk+'</td>';
                tr += '<td>' + isoDate+'</td>';
                tr += '<td>' + item.fields.path+'</td>';
                tr += '<td>' + item.fields.method+'</td>';
                tr += '<td>' + item.fields.user_agent+'</td>';
                tr += '<td>' + item.fields.remote_addr+'</td>';
                tr += '<td>' + item.fields.is_secure.toString().capitalize()+'</td>';
                tr += '<td>' + item.fields.is_ajax.toString().capitalize()+'</td>';
                tr += '</tr>';

                $(".table  > tbody > tr:first").before(tr);
            });

            for(var i = 0; i < (requests_in_response); i++) {
                $( ".table tbody tr:last-child" ).remove();
            }
        }

        if ( data.requests_quantity > 0 ) {

            var number_of_rows = $( ".table tbody" ).children().length;

            prepend_new_requests(new_requests, actual_number_of_requests, data.requests_quantity);

            setTimeout(unset_title, 5500, default_title);
        }
    });
  }, 7000);
});