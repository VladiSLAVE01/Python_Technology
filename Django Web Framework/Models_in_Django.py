# Вставьте сюда финальное содержимое файла models.py
from django.db import models


class SiteUser(models.Model):
    first_name = models.CharField(max_length=255)  # Поле для имени
    last_name = models.CharField(max_length=255)  # Поле для фамилии

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'site_users'  # Название таблицы в БД

    pass


class Vacancy(models.Model):
    name = models.TextField()  # Название вакансии
    salary = models.FloatField()  # Зарплата
    area_name = models.TextField()  # Город
    published_at = models.TextField()  # Дата публикации

    class Meta:
        db_table = 'vacancies'  # Название таблицы в БД
    pass

