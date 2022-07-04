$(document).ready(function() {
    $('#sidebar').on('show.bs.collapse hidden.bs.collapse', function() {
        $('.course-title').toggle();
    })
    // Basic DataTables
    $('#roles_table').DataTable({
        columnDefs: [{
            orderable: false,
            targets: -1
        }, ]
    })


    $('#specification_type_list, #active_borrow_request, #approved_borrow_request,#completed_borrow_request, #shelf_list, #store_list, #categories_list, #products_list, #labs_list, #table_list,  #specification_list').DataTable({
        columnDefs: [{
            orderable: false,
            targets: [0, -1]
        }, ]
    })
    $('#available_products_list').DataTable({
        dom: 'Qfltipr',
        responsive: true,
        columnDefs: [{
            orderable: false,
            targets: -1
        },
        { responsivePriority: 0, targets: 0},
        { responsivePriority: 1, targets: -1},
        { responsivePriority: 2, targets: [1, 2]},
        { responsivePriority: 3, targets: [3, 4]},
        ]
    })
    $('#department_list').DataTable({
        dom: 'QBfltipr',
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
    $('#colleges_list, #items_list').DataTable({
        dom: 'QBfltipr',
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

    document.querySelectorAll('#sidebar .nav-link').forEach(function(element){

    element.addEventListener('click', function (e) {

      let nextEl = element.nextElementSibling;
      let parentEl  = element.parentElement;

        if(nextEl) {
            e.preventDefault();
            let mycollapse = new bootstrap.Collapse(nextEl);

            if(nextEl.classList.contains('show')){
              mycollapse.hide();
            } else {
                mycollapse.show();
                // find other submenus with class=show
                var opened_submenu = parentEl.parentElement.querySelector('.submenu.show');
                // if it exists, then close all of them
                if(opened_submenu){
                  new bootstrap.Collapse(opened_submenu);
                }
            }
        }
    }); // addEventListener
  }) // forEach

})
