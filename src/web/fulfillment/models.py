from django.db import models
from common.models import BaseModel, SingletonModel


class MarkingPrice(SingletonModel):
    class Meta:
        verbose_name = "Маркировка"
        verbose_name_plural = "Маркировка"


class DoubleMarkingPrice(SingletonModel):
    class Meta:
        verbose_name = "Маркировка двойная"
        verbose_name_plural = "Маркировка двойная"


class StandardPackingPrice(SingletonModel):
    class Meta:
        verbose_name = "Упаковка Стандартная"
        verbose_name_plural = "Упаковка Стандартная"


class AssemblyPrice(SingletonModel):
    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборка"


class TaggingPrice(SingletonModel):
    class Meta:
        verbose_name = "Биркование"
        verbose_name_plural = "Биркование"


class InsertsPrice(SingletonModel):
    class Meta:
        verbose_name = "Вложения"
        verbose_name_plural = "Вложения"


class StackingPrice(SingletonModel):
    class Meta:
        verbose_name = "Укладка"
        verbose_name_plural = "Укладка"
