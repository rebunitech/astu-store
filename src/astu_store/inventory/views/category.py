from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from inventory.forms import CategoryForm, SubCategoryForm
from inventory.models import Category, SubCategory


class AddCategoryView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/add.html"
    success_url = reverse_lazy("inventory:categories_list")
    permission_required = ("inventory.add_category",)
    success_message = _("Category '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Category")}


class UpdateCategoryView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/update.html"
    success_url = reverse_lazy("inventory:categories_list")
    permission_required = ("inventory.change_category",)
    success_message = _("Category '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Category")}


class ListCategoriesView(PermissionRequiredMixin, ListView):
    model = Category
    context_object_name = "categories"
    permission_required = "inventory.view_category"
    extra_context = {"title": _("Categories")}
    template_name = "inventory/category/list.html"


class DeleteCategoryView(PermissionRequiredMixin, DeleteView):
    model = Category
    permission_required = ("inventory.delete_category",)
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:categories_list")


class AddSubCategoryView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "inventory/sub_category/add.html"
    success_url = reverse_lazy("inventory:sub_categories_list")
    permission_required = ("inventory.add_subcategory",)
    success_message = _("Sub category '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Subcategory")}


class UpdateSubCategoryView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "inventory/sub_category/update.html"
    success_url = reverse_lazy("inventory:sub_categories_list")
    permission_required = ("inventory.change_category",)
    success_message = _("Sub category '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Sub category")}


class ListSubCategoriesView(PermissionRequiredMixin, ListView):
    model = SubCategory
    context_object_name = "sub_categories"
    permission_required = "inventory.view_subcategory"
    extra_context = {"title": _("Sub categories")}
    template_name = "inventory/sub_category/list.html"


class DeleteSubCategoryView(PermissionRequiredMixin, DeleteView):
    model = SubCategory
    permission_required = ("inventory.delete_subcategory",)
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:sub_categories_list")
