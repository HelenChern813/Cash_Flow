from django.urls import path

from cash_flow import views
from cash_flow.apps import CashFlowConfig

app_name = CashFlowConfig.name

urlpatterns = [
    path("", views.CashFlowListView.as_view(), name="cashflow_list"),
    path("create/", views.CashFlowCreateView.as_view(), name="cashflow_create"),
    path("<int:pk>/edit/", views.CashFlowUpdateView.as_view(), name="cashflow_edit"),
    path("<int:pk>/delete/", views.CashFlowDeleteView.as_view(), name="cashflow_delete"),
    path("get-categories/", views.get_categories, name="get_categories"),
    path("get-subcategories/", views.get_subcategories, name="get_subcategories"),
    path("statuses/", views.StatusListView.as_view(), name="status_list"),
    path("statuses/create/", views.StatusCreateView.as_view(), name="status_create"),
    path("statuses/<int:pk>/edit/", views.StatusUpdateView.as_view(), name="status_edit"),
    path("statuses/<int:pk>/delete/", views.StatusDeleteView.as_view(), name="status_delete"),
    path("operation-types/", views.OperationTypeListView.as_view(), name="operation_type_list"),
    path("operation-types/create/", views.OperationTypeCreateView.as_view(), name="operation_type_create"),
    path("operation-types/<int:pk>/edit/", views.OperationTypeUpdateView.as_view(), name="operation_type_edit"),
    path("operation-types/<int:pk>/delete/", views.OperationTypeDeleteView.as_view(), name="operation_type_delete"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("subcategories/", views.SubcategoryListView.as_view(), name="subcategory_list"),
    path("subcategories/create/", views.SubcategoryCreateView.as_view(), name="subcategory_create"),
    path("subcategories/<int:pk>/edit/", views.SubcategoryUpdateView.as_view(), name="subcategory_edit"),
    path("subcategories/<int:pk>/delete/", views.SubcategoryDeleteView.as_view(), name="subcategory_delete"),
]
