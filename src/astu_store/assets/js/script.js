$(document).ready(function() {
    $('#sidebar').on('show.bs.collapse hidden.bs.collapse', function() {
        $('.course-title').toggle();
    })
    $('#specification_type_list, #shelf_list, #specification_list').DataTable({
        columnDefs: [{
            orderable: false,
            targets: [0, -1]
        }, ]
    })
    $('#store_list, #item_list, #department_list').DataTable({
        dom: 'Qfltipr',
        columnDefs: [{
            orderable: false,
            targets: -1
        },
        { responsivePriority: 0, targets: 1},
        { responsivePriority: 1, targets: -1},
        { responsivePriority: 2, targets: [3, 4, 5, 6, 7, 8]},
        { responsivePriority: 3, targets: 2},
        ]
    })
    $('#colleges_list').DataTable({
        dom: 'Qfltipr',
        responsive: true,
        columnDefs: [{
            orderable: false,
            targets: -1
        },
        { responsivePriority: 0, targets: 1},
        { responsivePriority: 1, targets: -1},
        { responsivePriority: 2, targets: [3, 4, 5, 6, 7]},
        { responsivePriority: 3, targets: 0},
        { responsivePriority: 4, targets: 2}
        ]
    })
    $('[id*=_wrapper] label').addClass('d-flex flex-row align-items-center')
    $('[id*=_wrapper] label > *').addClass('mx-2')
    $('[id*=_wrapper]').addClass('shadow')
    $('[id*=_wrapper] > div:first-child').addClass('bg-secondary text-light')
    $('[id*=_wrapper] > div').addClass('p-2 px-4 my-1 rounded-top')
    $('[id*=_wrapper] select, [id*=_wrapper] input').addClass('form-control shadow-none')
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

})