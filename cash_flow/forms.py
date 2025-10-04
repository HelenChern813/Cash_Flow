from django import forms

from .models import CashFlow, Category, OperationType, Status, Subcategory


class CashFlowForm(forms.ModelForm):
    """Форма для создания и редактирования записей ДДС"""

    class Meta:
        model = CashFlow
        fields = ["date", "status", "operation_type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control", "required": True}),
            "status": forms.Select(attrs={"class": "form-control", "required": True}),
            "operation_type": forms.Select(
                attrs={"class": "form-control", "required": True, "id": "id_operation_type"}
            ),
            "category": forms.Select(attrs={"class": "form-control", "required": True, "id": "id_category"}),
            "subcategory": forms.Select(attrs={"class": "form-control", "required": True, "id": "id_subcategory"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0.01", "required": True, "placeholder": "0.00"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Необязательный комментарий..."}
            ),
        }
        labels = {
            "date": "Дата операции",
            "status": "Статус",
            "operation_type": "Тип операции",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "amount": "Сумма (руб)",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Для существующей записи ограничиваем выбор категорий и подкатегорий
        if self.instance and self.instance.pk:
            if self.instance.operation_type:
                self.fields["category"].queryset = Category.objects.filter(operation_type=self.instance.operation_type)
            if self.instance.category:
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            self.fields["category"].queryset = Category.objects.all()
            self.fields["subcategory"].queryset = Subcategory.objects.all()

            if self.initial.get("operation_type"):
                operation_type = self.initial["operation_type"]
                self.fields["category"].queryset = Category.objects.filter(operation_type=operation_type)

            if self.initial.get("category"):
                category = self.initial["category"]
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category=category)

    def clean(self):
        """Дополнительная валидация на уровне формы"""

        cleaned_data = super().clean()

        operation_type = cleaned_data.get("operation_type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category and operation_type:
            if category.operation_type != operation_type:
                self.add_error("category", "Выбранная категория не принадлежит выбранному типу операции")

        if subcategory and category:
            if subcategory.category != category:
                self.add_error("subcategory", "Выбранная подкатегория не принадлежит выбранной категории")

        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для статусов"""

    class Meta:
        model = Status
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class OperationTypeForm(forms.ModelForm):
    """Форма для типов операций"""

    class Meta:
        model = OperationType
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CategoryForm(forms.ModelForm):
    """Форма для категорий"""

    class Meta:
        model = Category
        fields = ["name", "operation_type", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "operation_type": forms.Select(attrs={"class": "form-control", "required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для подкатегорий"""

    class Meta:
        model = Subcategory
        fields = ["name", "category", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "category": forms.Select(attrs={"class": "form-control", "required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
