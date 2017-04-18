require([
    'jquery',
    '++plone++cmo/datatables/js/jquery.dataTables.min.js'
], function($){

$(document).ready(function() {
    var table = $('#workshoptable').DataTable( {       
        "scrollY": "600px",
        "paging": false,
        // "sScrollY": "600px",
        // "bPaginate": false,
        // "bScrollCollapse": true,
        "bAutoWidth": true,
        // "info":     false,
        "searching": false,
        // "sScrollX": "100%",
        // "sScrollXInner": "100%",
    } );
    $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();
 
        // Get the column API object
        var column = table.column( $(this).attr('data-column') );
 
        // Toggle the visibility
        column.visible( ! column.visible() );
    } );
});

});