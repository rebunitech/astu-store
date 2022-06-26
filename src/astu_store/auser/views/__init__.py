from .college import (ActivateCollegeView, AddCollegeView, CollegeDetailView,
                      DeactivateCollegeView, DeleteCollegeView,
                      ListCollegesView, UpdateCollegeView)
from .college_representative import (AddCollegeRepresentativeView,
                                     AssignCollegeRepresentativeView,
                                     CollegeRepresentativeActivateView,
                                     CollegeRepresentativeDeactivateView,
                                     CollegeRepresentativeDeleteView,
                                     CollegeRepresentativesListView,
                                     CollegeRepresentativeUpdateView,
                                     RemoveFromCollegeRepresentativeView)
from .department import (ActivateDepartmentView, AddDepartmentView,
                         DeactivateDepartmentView, DeleteDepartmentView,
                         ListDepartmentsOfCollegeView, UpdateDepartmentView)
from .department_representative import AddDepartmentRepresentativeView
from .user import (ActivateUserView, DeactivateUserView, DeleteUserView,
                   UpdateUserView)
from .view import DashboardView


__all__ = [
	'ActivateCollegeView',
	'AddCollegeView',
	'CollegeDetailView',
	'DeactivateCollegeView',
	'DeleteCollegeView',
	'ListCollegesView',
	'UpdateCollegeView',
	'AddCollegeRepresentativeView',
	'AssignCollegeRepresentativeView',
	'CollegeRepresentativeActivateView',
	'CollegeRepresentativeDeactivateView',
	'CollegeRepresentativeDeleteView',
	'CollegeRepresentativesListView',
	'CollegeRepresentativeUpdateView',
	'RemoveFromCollegeRepresentativeView',
	'ActivateDepartmentView',
	'AddDepartmentView',
	'DeactivateDepartmentView',
	'DeleteDepartmentView',
	'ListDepartmentsOfCollegeView',
	'UpdateDepartmentView',
	'AddDepartmentRepresentativeView',
	'ActivateUserView',
	'DeactivateUserView',
	'DeleteUserView',
	'UpdateUserView',
	'DashboardView',
]