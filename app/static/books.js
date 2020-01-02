$(document).ready( function () {
    $.ajax({
        url: "/api/books",
        type: "GET",
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
    }).done(function(data){

        var columns = [{
                data: "book_id",
                title: "No",
                type: "readonly"
            }, {
                data: "title",
                title: "Title"
            }, {
                data: "author",
                title: "Author"
            }, {
                data: "publisher",
                title: "Publisher"
            }, {
                data: "book_owner",
                title: "Book Owner"
            }, {
                data: "isbn",
                title: "ISBN"
            }, {
                data: "pages",
                title: "Pages"
            }, {
                data: "category",
                title: "Genre"
            }, {
                data: "description",
                title: "Details"
            }, {
                data: "state",
                title: "Status",
                type : "select",
                options: ["Available", "Rent"]
        }];

        $('#table').DataTable({
            select: true,
            deferRender:    true,
            scrollY:        600,
            scrollCollapse: true,
            scroller:       true,
            data: data.books,
            columns: columns,
            dom: 'Bfrtip',        // Needs button container
            select: 'single',
            responsive: true,
            altEditor: true,     // Enable altEditor
            buttons: [{
                text: 'Add',
                name: 'add'        // do not change name
            },
            {
                extend: 'selected', // Bind to Selected row
                text: 'Edit',
                name: 'edit'        // do not change name
            },
            {
                extend: 'selected', // Bind to Selected row
                text: 'Delete',
                name: 'delete'      // do not change name
            }],
            onAddRow: function(datatable, rowdata, success, error) {
                $.ajax({
                    cache: false,
                    url: '/book/add',
                    type: 'POST',
                    data: rowdata,
                    success: success,
                    error: error
                });
            },
            onDeleteRow: function(datatable, rowdata, success, error) {
                $.ajax({
                    url: '/book/delete',
                    type: 'DELETE',
                    data: rowdata,
                    success: success,
                    error: error
                });
            },
            onEditRow: function(datatable, rowdata, success, error) {
                $.ajax({
                    url: '/book/edit',
                    type: 'POST',
                    data: rowdata,
                    success: success,
                    error: error
                });
            }
        });
    });
} );