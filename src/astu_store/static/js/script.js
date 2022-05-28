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
    $('#store_list, #item_list, #colleges_list').DataTable({
        dom: 'Qfltipr',
        columnDefs: [{
            orderable: false,
            targets: [0, -1]
        }, ]
    })
    $('[id*=_wrapper] label').addClass('d-flex flex-row align-items-center')
    $('[id*=_wrapper] label > *').addClass('mx-2')
    $('[id*=_wrapper]').addClass('shadow')
    $('[id*=_wrapper] > div:first-child').addClass('bg-secondary text-light')
    $('[id*=_wrapper] > div').addClass('p-2 px-4 my-1 rounded-top')
    $('[id*=_wrapper] select, [id*=_wrapper] input').addClass('form-control shadow-none')
})