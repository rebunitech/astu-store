function format(d) {
    return '<table class ="table table-stripped w-auto">' +
        '<tr><img src="' + d[7] + '" class="img-fluid mx-5" style="width:100px;"></tr>' +
        '<tr><td>Last login:</td>' +
        '<td><strong>' + d[8] + '</strong></td>' +
        '</tr><tr><td>Date joined:</td>' +
        '<td><strong>' + d[9] + '</strong></td>' +
        '</tr><tr><td>' + d[10] + '</td></tr></table>';
}

$(document).ready(function() {
    let table = $('#dt_table_staff, #dt_table_content_creator, #dt_table_student').DataTable({
        dom: 'BQfltipr',
        buttons: [{
                extend: 'csv',
                className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded',
                text: 'CSV',
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6],
                },
            },
            {
                extend: 'excel',
                className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded',
                text: 'Excel',
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6],
                },
            },
            {
                extend: 'pdf',
                className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded',
                text: 'PDF',
                orientation: "landscape",
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6],
                },
                header: true,
                footer: true,
                customize: function(pdf) {
                    pdf.header = function(pageSize) {
                        return [
                            { text: 'Date: ' + new Date().toDateString(), alignment: 'right', margin: [0, 25, 20, 0] },
                        ]
                    };
                    pdf.footer = function(currentPage, pageCount) {
                        return [
                            { text: 'Page ' + currentPage.toString() + ' of ' + pageCount, alignment: 'center', },
                        ]
                    };
                    pdf.content[1].table.widths = ["*", "*", "*", "*", "auto", 'auto'];
                    pdf.content[1].layout = {
                        paddingLeft: function(i, node) { return 5; },
                        paddingRight: function(i, node) { return 5; },
                    }
                    pdf.styles.tableBodyOdd.margin = [0, 1, 0, 1];
                    pdf.styles.tableBodyEven.margin = [0, 1, 0, 1];
                }
            },
        ],
        responsive: {
            details: {
                type: 'column'
            }
        },
        columnDefs: [{
                orderable: false,
                targets: 0
            },
            { targets: [7, 8, 9, 10], className: 'never' },
        ],
        stateSave: false,
        select: {
            style: 'os',
            selector: 'td:nth-child(n+2):nth-child(-n+7)'
        }
    });

    $('#dt_table_staff tbody, #dt_table_content_creator tbody, #dt_table_student').on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    })
    $('#dt_table_user_actions').DataTable({
        dom: 'BQfltipr',
        buttons: [
            { extend: 'csv', className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded', text: 'CSV' },
            { extend: 'excel', className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded', text: 'Excel' },
            {
                extend: 'pdf',
                className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded',
                text: 'PDF',
                orientation: "landscape",
                exportOptions: {
                    columns: [1, 2, 3, 4],
                },
                header: true,
                footer: true,
                customize: function(pdf) {
                    pdf.header = function(pageSize) {
                        return [
                            { text: 'Date: ' + new Date().toDateString(), alignment: 'right', margin: [0, 25, 20, 0] },
                        ]
                    };
                    pdf.footer = function(currentPage, pageCount) {
                        return [
                            { text: 'Page ' + currentPage.toString() + ' of ' + pageCount, alignment: 'center', },
                        ]
                    };
                    pdf.content[1].table.widths = ["*", "*", "*", "*", "*"];
                    pdf.content[1].layout = {
                        paddingLeft: function(i, node) { return 5; },
                        paddingRight: function(i, node) { return 5; },
                    }
                    pdf.styles.tableBodyOdd.margin = [0, 1, 0, 1];
                    pdf.styles.tableBodyEven.margin = [0, 1, 0, 1];
                }
            },
        ],
        responsive: {
            details: {
                type: 'column'
            }
        },
        columnDefs: [{
            orderable: false,
            targets: 0
        }, ],
        stateSave: false,
        select: true
    });

    $('#dt_table_user_history').DataTable({
        dom: 'BQfltipr',
        buttons: [
            { extend: 'csv', className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded', text: 'CSV' },
            { extend: 'excel', className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded', text: 'Excel' },
            {
                extend: 'pdf',
                className: 'btn btn-sm btn-dark mx-1 px-3 shadow-none rounded',
                text: 'PDF',
                orientation: "landscape",
                exportOptions: {
                    columns: [1, 2, 3],
                },
                header: true,
                footer: true,
                customize: function(pdf) {
                    pdf.header = function(pageSize) {
                        return [
                            { text: 'Date: ' + new Date().toDateString(), alignment: 'right', margin: [0, 25, 20, 0] },
                        ]
                    };
                    pdf.footer = function(currentPage, pageCount) {
                        return [
                            { text: 'Page ' + currentPage.toString() + ' of ' + pageCount, alignment: 'center', },
                        ]
                    };
                    pdf.content[1].table.widths = ["*", "*", "*", ];
                    pdf.content[1].layout = {
                        paddingLeft: function(i, node) { return 5; },
                        paddingRight: function(i, node) { return 5; },
                    }
                    pdf.styles.tableBodyOdd.margin = [0, 1, 0, 1];
                    pdf.styles.tableBodyEven.margin = [0, 1, 0, 1];
                }
            },
        ],
        responsive: {
            details: {
                type: 'column'
            }
        },
        columnDefs: [{
            orderable: false,
            targets: 0
        }, ],
        stateSave: false,
        select: true
    });

    $('#dt_table_social_link, #dt_table_social_media').DataTable({})
    document.querySelectorAll('.choices').forEach(choice => {
        if (choice.classList.contains("multiple-remove")) {
            var initChoice = new Choices(choice, {
                delimiter: ',',
                editItems: true,
                maxItemCount: -1,
                removeItemButton: true,
            });
        } else {
            var initChoice = new Choices(choice);
        }
    });
    feather.replace();
});

//