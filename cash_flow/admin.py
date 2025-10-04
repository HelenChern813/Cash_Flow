from django.contrib import admin

from .models import CashFlow, Category, OperationType, Status, Subcategory


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "operation_type", "description"]
    list_filter = ["operation_type"]
    search_fields = ["name"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "description"]
    list_filter = ["category", "category__operation_type"]
    search_fields = ["name"]


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ["date", "status", "operation_type", "category", "subcategory", "amount", "comment"]
    list_filter = ["date", "status", "operation_type", "category"]
    search_fields = ["comment", "category__name", "subcategory__name"]
    date_hierarchy = "date"
    ordering = ["-date"]
