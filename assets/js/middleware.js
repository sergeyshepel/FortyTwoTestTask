String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function sortTable(table_body, order) {
    table_body.find('tr').sort(function(a,b){
        var tda = $(a).find('td:eq(1)').text();
        var tdb = $(b).find('td:eq(1)').text();
        if (order === 0) {
            return tda > tdb ? 1
                   : tda < tdb ? -1
                   : 0;
        } else {
            return tda < tdb ? 1
                   : tda > tdb ? -1
                   : 0;
        }
    }).appendTo(table_body);
}

$( function() {
    // asc
    $( "#requests_table" ).on( "click", "th.headerSortDown", function(){
        $(this).toggleClass("headerSortDown headerSortUp");
        sortTable($("#requests_table tbody"), 0);
    });
    // desc
    $( "#requests_table" ).on( "click", "th.headerSortUp", function(){
        $(this).toggleClass("headerSortUp headerSortDown");
        sortTable($("#requests_table tbody"), 1);
    });
    // ajax
    setInterval( function() {
        var ids=[];

        // iterate all td's in hidden id column
        $('#requests_table tbody tr td:nth-child(1)').each( function(){
            //add item to array
            ids.push( $(this).text() );
        });

        var latest_id = Math.max.apply(Math, ids);

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
                    tr += '<td>' + item.fields.priority+'</td>';
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

                // sort
                var priorityClassName = $('#requests_table th:nth-child(2)').attr('class');
                if (priorityClassName === 'headerSortDown'){
                    sortTable($("#requests_table tbody"), 1);
                } else if (priorityClassName === 'headerSortUp') {
                    sortTable($("#requests_table tbody"), 0);
                }
                setTimeout(unset_title, 5500, default_title);
            }
        });
    }, 7000);
});