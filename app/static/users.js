$(document).ready( function () {
    $.ajax({
        url: "/api/users",
        type: "GET",
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
    }).done(function(data){

        var columns = [{
                data: "user_id",
                title: "No",
                type: "readonly"
            }, {
                data: "name",
                title: "Name"
            }, {
                data: "surname",
                title: "Surname"
            }, {
                data: "mail",
                title: "E-mail"
            }, {
                data: "phone",
                title: "Phone number"
            }];

        $('#table').DataTable({
            select: true,
            deferRender:    true,
            scrollY:        600,
            scrollCollapse: true,
            scroller:       true,
            data: data.users,
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
                    url: '/user/add',
                    type: 'POST',
                    data: rowdata,
                    success: success,
                    error: error
                });
            },
            onDeleteRow: function(datatable, rowdata, success, error) {
                $.ajax({
                    url: '/user/delete',
                    type: 'DELETE',
                    data: rowdata,
                    success: success,
                    error: error
                });
            },
            onEditRow: function(datatable, rowdata, success, error) {
                $.ajax({
                    url: '/user/edit',
                    type: 'POST',
                    data: rowdata,
                    success: success,
                    error: error
                });
            }
        });
    });
} );