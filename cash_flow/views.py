from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CashFlowForm, CategoryForm, OperationTypeForm, StatusForm, SubcategoryForm
from .models import CashFlow, Category, OperationType, Status, Subcategory


class CashFlowListView(ListView):
    """Главная страница - список записей ДДС с фильтрацией"""

    model = CashFlow
    template_name = "cashflow/cashflow_list.html"
    context_object_name = "cashflows"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по дате
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Фильтрация по статусу
        status_id = self.request.GET.get("status")
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        # Фильтрация по типу операции
        operation_type_id = self.request.GET.get("operation_type")
        if operation_type_id:
            queryset = queryset.filter(operation_type_id=operation_type_id)

        # Фильтрация по категории
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Фильтрация по подкатегории
        subcategory_id = self.request.GET.get("subcategory")
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["operation_types"] = OperationType.objects.all()
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()

        # Сохраняем параметры фильтрации для формы
        context["filter_params"] = {
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "status": self.request.GET.get("status", ""),
            "operation_type": self.request.GET.get("operation_type", ""),
            "category": self.request.GET.get("category", ""),
            "subcategory": self.request.GET.get("subcategory", ""),
        }

        return context


class CashFlowCreateView(CreateView):
    """Создание новой записи ДДС"""

    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")

    def form_valid(self, form):

        return super().form_valid(form)


class CashFlowUpdateView(UpdateView):
    """Редактирование записи ДДС"""

    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")


class CashFlowDeleteView(DeleteView):
    """Удаление записи ДДС"""

    model = CashFlow
    template_name = "cashflow/cashflow_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")


def get_subcategories(request):
    """AJAX-функция для получения подкатегорий по выбранной категории"""

    category_id = request.GET.get("category_id")
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id)
        data = [{"id": sub.id, "name": sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def get_categories(request):
    """AJAX-функция для получения категорий по выбранному типу операции"""

    operation_type_id = request.GET.get("operation_type_id")
    if operation_type_id:
        categories = Category.objects.filter(operation_type_id=operation_type_id)
        data = [{"id": cat.id, "name": cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


class StatusListView(ListView):
    model = Status
    template_name = "cashflow/reference_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Status"
        context["title"] = "Управление статусами"
        context["create_url"] = "cash_flow:status_create"
        context["edit_url_name"] = "cash_flow:status_edit"
        context["delete_url_name"] = "cash_flow:status_delete"
        return context


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статуса"
        context["back_url"] = "cash_flow:status_list"
        return context


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование статуса"
        context["back_url"] = "cash_flow:status_list"
        return context


class StatusDeleteView(DeleteView):
    model = Status
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление статуса"
        context["back_url"] = "cash_flow:status_list"
        context["model_name"] = "Status"
        return context


class OperationTypeListView(ListView):
    model = OperationType
    template_name = "cashflow/reference_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "OperationType"
        context["title"] = "Управление типами операций"
        context["create_url"] = "cash_flow:operation_type_create"
        context["edit_url_name"] = "cash_flow:operation_type_edit"
        context["delete_url_name"] = "cash_flow:operation_type_delete"
        return context


class OperationTypeCreateView(CreateView):
    model = OperationType
    form_class = OperationTypeForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        return context


class OperationTypeUpdateView(UpdateView):
    model = OperationType
    form_class = OperationTypeForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        return context


class OperationTypeDeleteView(DeleteView):
    model = OperationType
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        context["model_name"] = "OperationType"
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "cashflow/reference_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Category"
        context["title"] = "Управление категориями"
        context["create_url"] = "cash_flow:category_create"
        context["edit_url_name"] = "cash_flow:category_edit"
        context["delete_url_name"] = "cash_flow:category_delete"
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление категории"
        context["back_url"] = "cash_flow:category_list"
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование категории"
        context["back_url"] = "cash_flow:category_list"
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление категории"
        context["back_url"] = "cash_flow:category_list"
        context["model_name"] = "Category"
        return context


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = "cashflow/reference_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Subcategory"
        context["title"] = "Управление подкатегориями"
        context["create_url"] = "cash_flow:subcategory_create"
        context["edit_url_name"] = "cash_flow:subcategory_edit"
        context["delete_url_name"] = "cash_flow:subcategory_delete"
        return context


class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        return context


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        return context


class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        context["model_name"] = "Subcategory"
        return context
