from django.db import models
import hashlib
import datetime


class MyUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "my_user"

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password == self.hash_password(password)

    @staticmethod
    def verify_age(age):
        try:
            return 18 <= int(age) <= 150
        except ValueError:
            return False

    @property
    def skills(self):
        return [user_skill.skill.name for user_skill in UserSkill.objects.filter(user=self)]


class Vacancy(models.Model):
    name = models.TextField()
    salary = models.IntegerField()
    area_name = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'vacancy'

    @property
    def skills(self):
        return [vacancy_skill.skill.name for vacancy_skill in VacancySkill.objects.filter(vacancy=self)]


class Skill(models.Model):
    name = models.CharField("Имя", max_length=64)

    class Meta:
        db_table = 'skill'

    @classmethod
    def get_all_skills(cls):
        return cls.objects.all()


class VacancySkill(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vacancy_skill'
        unique_together = ('vacancy', 'skill')


class UserSkill(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_skill'
        unique_together = ('user', 'skill')


class UserResponse(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        db_table = 'user_response'