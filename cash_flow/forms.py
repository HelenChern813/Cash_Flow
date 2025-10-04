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
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Ограничиваем выбор только пользовательскими данными
        if self.user:
            self.fields["status"].queryset = Status.objects.filter(user=self.user)
            self.fields["operation_type"].queryset = OperationType.objects.filter(user=self.user)
            self.fields["category"].queryset = Category.objects.filter(user=self.user)
            self.fields["subcategory"].queryset = Subcategory.objects.filter(user=self.user)

        # Для существующей записи ограничиваем выбор категорий и подкатегорий
        if self.instance and self.instance.pk:
            if self.instance.operation_type:
                self.fields["category"].queryset = Category.objects.filter(
                    operation_type=self.instance.operation_type, user=self.user
                )
            if self.instance.category:
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category=self.instance.category, user=self.user
                )
        else:
            self.fields["category"].queryset = Category.objects.filter(user=self.user)
            self.fields["subcategory"].queryset = Subcategory.objects.filter(user=self.user)

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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    # def clean_name(self):
    #     """Проверка уникальности имени статуса в рамках пользователя"""
    #
    #     name = self.cleaned_data.get('name')
    #     if self.user and name:
    #
    #         existing_status = Status.objects.filter(name=name, user=self.user)
    #         if self.instance and self.instance.pk:
    #             existing_status = existing_status.exclude(pk=self.instance.pk)
    #         if existing_status.exists():
    #             raise forms.ValidationError("Статус с таким названием уже существует у вас.")
    #     return name


class OperationTypeForm(forms.ModelForm):
    """Форма для типов операций"""

    class Meta:
        model = OperationType
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    # def clean_name(self):
    #     """Проверка уникальности имени типа операции в рамках пользователя"""
    #
    #     name = self.cleaned_data.get('name')
    #     if self.user and name:
    #         existing_operation_type = OperationType.objects.filter(name=name, user=self.user)
    #         if self.instance and self.instance.pk:
    #             existing_operation_type = existing_operation_type.exclude(pk=self.instance.pk)
    #         if existing_operation_type.exists():
    #             raise forms.ValidationError("Тип операции с таким названием уже существует у вас.")
    #     return name


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["operation_type"].queryset = OperationType.objects.filter(user=self.user)


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["category"].queryset = Category.objects.filter(user=self.user)
