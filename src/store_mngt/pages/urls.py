from django.urls import include, re_path
from pages import views

app_name = "pages"

urlpatterns = [
    re_path(r"", include("django.contrib.auth.urls")),

    # flatpages urls
    re_path(r"^flatpage/$", views.ListFlatPageView.as_view(), name="list-flatpage"),
    re_path(r"^flatpage/add/$", views.AddFlatPageView.as_view(), name="add-flatpage"),
    re_path(
        r"^flatpage/update/(?P<pk>\d+)/$",
        views.UpdateFlatPageView.as_view(),
        name="update-flatpage",
    ),
    re_path(
        r"^flatpage/delete/(?P<pk>\d+)/$",
        views.DeleteFlatPageView.as_view(),
        name="delete-flatpage",
    ),


    re_path(r"^dashboard/$", views.DashboardView.as_view(), name="dashboard"),    
]
