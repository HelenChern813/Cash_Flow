from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CashFlowForm, CategoryForm, OperationTypeForm, StatusForm, SubcategoryForm
from .models import CashFlow, Category, OperationType, Status, Subcategory


class UserAccessMixin(LoginRequiredMixin):
    """Миксин для проверки доступа пользователя"""

    def get_queryset(self):
        """Возвращает только объекты текущего пользователя"""
        if hasattr(self, "model"):
            return self.model.objects.filter(user=self.request.user)
        return super().get_queryset()


class CashFlowListView(UserAccessMixin, ListView):
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
        user = self.request.user
        context["statuses"] = Status.objects.filter(user=user)
        context["operation_types"] = OperationType.objects.filter(user=user)
        context["categories"] = Category.objects.filter(user=user)
        context["subcategories"] = Subcategory.objects.filter(user=user)

        context["filter_params"] = {
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "status": self.request.GET.get("status", ""),
            "operation_type": self.request.GET.get("operation_type", ""),
            "category": self.request.GET.get("category", ""),
            "subcategory": self.request.GET.get("subcategory", ""),
        }

        return context


class CashFlowCreateView(UserAccessMixin, CreateView):
    """Создание новой записи ДДС"""

    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Запись успешно создана!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class CashFlowUpdateView(UserAccessMixin, UpdateView):
    """Редактирование записи ДДС"""

    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Запись успешно обновлена!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class CashFlowDeleteView(UserAccessMixin, DeleteView):
    """Удаление записи ДДС"""

    model = CashFlow
    template_name = "cashflow/cashflow_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:cashflow_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Запись успешно удалена!")
        return super().delete(request, *args, **kwargs)


def get_subcategories(request):
    """AJAX-функция для получения подкатегорий по выбранной категории"""

    category_id = request.GET.get("category_id")
    if category_id and request.user.is_authenticated:
        subcategories = Subcategory.objects.filter(category_id=category_id, user=request.user)
        data = [{"id": sub.id, "name": sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def get_categories(request):
    """AJAX-функция для получения категорий по выбранному типу операции"""

    operation_type_id = request.GET.get("operation_type_id")
    if operation_type_id and request.user.is_authenticated:
        categories = Category.objects.filter(operation_type_id=operation_type_id, user=request.user)
        data = [{"id": cat.id, "name": cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


class StatusListView(UserAccessMixin, ListView):
    """Отображение списка статусов"""

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


class StatusCreateView(UserAccessMixin, CreateView):
    """Создание нового статуса"""

    model = Status
    form_class = StatusForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Статус успешно создан!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статуса"
        context["back_url"] = "cash_flow:status_list"
        return context


class StatusUpdateView(UserAccessMixin, UpdateView):
    """Редактирование статуса"""

    model = Status
    form_class = StatusForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно обновлен!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование статуса"
        context["back_url"] = "cash_flow:status_list"
        return context


class StatusDeleteView(UserAccessMixin, DeleteView):
    """Удаление статуса"""

    model = Status
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:status_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Статус успешно удален!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление статуса"
        context["back_url"] = "cash_flow:status_list"
        context["model_name"] = "Status"
        return context


class OperationTypeListView(UserAccessMixin, ListView):
    """Отображение списка типов операций"""

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


class OperationTypeCreateView(UserAccessMixin, CreateView):
    """Создаение типа операции"""

    model = OperationType
    form_class = OperationTypeForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Тип операции успешно создан!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        return context


class OperationTypeUpdateView(UserAccessMixin, UpdateView):
    """Редактирование типа операций"""

    model = OperationType
    form_class = OperationTypeForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Тип операции успешно обновлен!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        return context


class OperationTypeDeleteView(UserAccessMixin, DeleteView):
    """Удаление типа операции"""

    model = OperationType
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:operation_type_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Тип операции успешно удален!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление типа операции"
        context["back_url"] = "cash_flow:operation_type_list"
        context["model_name"] = "OperationType"
        return context


class CategoryListView(UserAccessMixin, ListView):
    """Отображение списка категорий"""

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


class CategoryCreateView(UserAccessMixin, CreateView):
    """Создание новой категории"""

    model = Category
    form_class = CategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Категория успешно создана!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление категории"
        context["back_url"] = "cash_flow:category_list"
        return context


class CategoryUpdateView(UserAccessMixin, UpdateView):
    """Редактирование категории"""

    model = Category
    form_class = CategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно обновлена!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование категории"
        context["back_url"] = "cash_flow:category_list"
        return context


class CategoryDeleteView(UserAccessMixin, DeleteView):
    """Удаление категории"""

    model = Category
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:category_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Категория успешно удалена!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление категории"
        context["back_url"] = "cash_flow:category_list"
        context["model_name"] = "Category"
        return context


class SubcategoryListView(UserAccessMixin, ListView):
    """Отображение списка подкатегорий"""

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


class SubcategoryCreateView(UserAccessMixin, CreateView):
    """Создание новой подкатегории"""

    model = Subcategory
    form_class = SubcategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Подкатегория успешно создана!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        return context


class SubcategoryUpdateView(UserAccessMixin, UpdateView):
    """Редактирование подкатегории"""

    model = Subcategory
    form_class = SubcategoryForm
    template_name = "cashflow/reference_form.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Подкатегория успешно обновлена!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        return context


class SubcategoryDeleteView(UserAccessMixin, DeleteView):
    """Удаление подкатегории"""

    model = Subcategory
    template_name = "cashflow/reference_confirm_delete.html"
    success_url = reverse_lazy("cash_flow:subcategory_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Подкатегория успешно удалена!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление подкатегории"
        context["back_url"] = "cash_flow:subcategory_list"
        context["model_name"] = "Subcategory"
        return context
