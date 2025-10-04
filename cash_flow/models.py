from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Status(models.Model):
    """Модель статусов (Бизнес, Личное, Налог)"""

    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название статуса", help_text="Пример: Бизнес, Личное, Налог, другое"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Описание статуса")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class OperationType(models.Model):
    """Модель типов операций (Пополнение, Списание)"""

    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название типа операции", help_text="Пополнение / Списание"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание типа оперции, если нужно"
    )

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории операций (привязаны к типам)"""

    name = models.CharField(max_length=100, verbose_name="Название категории", help_text="Введите название категории")

    operation_type = models.ForeignKey(OperationType, on_delete=models.CASCADE, verbose_name="Тип операции")

    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ["name", "operation_type"]

    def __str__(self):
        return f"{self.name} ({self.operation_type})"


class Subcategory(models.Model):
    """Подкатегории операций (привязаны к категориям)"""

    name = models.CharField(
        max_length=100, verbose_name="Название подкатегории", help_text="Введите название подкатегории"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(blank=True, verbose_name="Описание", help_text="Введите описание подкатегории")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ["name", "category"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class CashFlow(models.Model):
    """Записи движения денежных средств"""

    date = models.DateField(default=timezone.now, verbose_name="Дата операции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    operation_type = models.ForeignKey(OperationType, on_delete=models.PROTECT, verbose_name="Тип операции")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-date", "-created_at"]

    def clean(self):
        """Валидация логических зависимостей"""

        if (
            self.operation_type_id
            and self.category_id
            and hasattr(self, "category")
            and hasattr(self, "operation_type")
        ):
            if self.category.operation_type_id != self.operation_type_id:
                raise ValidationError({"category": "Выбранная категория не принадлежит выбранному типу операции"})

        if self.category_id and self.subcategory_id and hasattr(self, "subcategory") and hasattr(self, "category"):
            if self.subcategory.category_id != self.category_id:
                raise ValidationError({"subcategory": "Выбранная подкатегория не принадлежит выбранной категории"})

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова валидации"""

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.operation_type} - {self.amount} руб."
