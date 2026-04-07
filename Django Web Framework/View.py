from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser , Vacancy, Skill, UserResponse, VacancySkill, UserSkill

@csrf_exempt
def add_user(request):
    try:
        if request.method == 'POST':
            data = request.POST
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            age = int(data.get('age'))
            email = data.get('email')
            password = data.get('password')

            if not MyUser .verify_age(age):
                raise ValueError("Age must be greater than 18 and lower than 122!")

            user = MyUser (first_name=first_name, last_name=last_name,
                           age=age, email=email, password=MyUser .hash_password(password))
            user.save()

            return render(request, 'answer.html', {'answer': user.id})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def delete_user(request):
    try:
        if request.method == 'POST':
            data = request.POST
            email = data.get('email')
            password = data.get('password')

            user = MyUser .objects.get(email=email)
            if not user.verify_password(password):
                return render(request, 'error.html', {'error': 'Wrong password'})

            user.delete()
            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def authorise(request):
    try:
        if request.method == 'POST':
            data = request.POST
            email = data.get('email')
            password = data.get('password')

            user = MyUser .objects.get(email=email)
            if not user.verify_password(password):
                return render(request, 'error.html', {'error': 'Wrong password'})

            return render(request, 'user_info.html', {'user': user, 'skills': user.skills})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def add_vacancy(request):
    try:
        if request.method == 'POST':
            data = request.POST
            name = data.get('name')
            salary = int(data.get('salary'))
            area_name = data.get('area_name')

            vacancy = Vacancy(name=name, salary=salary, area_name=area_name)
            vacancy.save()

            return render(request, 'answer.html', {'answer': vacancy.id})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def get_vacancy(request):
    try:
        vacancy_id = request.GET.get('id')
        vacancy = Vacancy.objects.get(id=vacancy_id)

        return render(request, 'vacancy.html', {
            'vacancy': vacancy,
            'skills': vacancy.skills,
            'responses': UserResponse.objects.filter(vacancy=vacancy)
        })
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def delete_vacancy(request):
    try:
        if request.method == 'POST':
            data = request.POST
            vacancy_id = data.get('id')

            Vacancy.objects.get(id=vacancy_id).delete()
            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def add_skill(request):
    try:
        if request.method == 'POST':
            data = request.POST
            name = data.get('name')

            skill = Skill(name=name)
            skill.save()

            return render(request, 'answer.html', {'answer': skill.id})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def get_skill(request):
    try:
        if request.method == 'POST':
            skill_id = request.POST.get('id')
            skill = Skill.objects.get(id=skill_id)

            return render(request, 'answer.html', {'answer': skill.name})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def delete_skill(request):
    try:
        if request.method == 'POST':
            skill_id = request.POST.get('id')
            Skill.objects.get(id=skill_id).delete()

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def get_all_skills(request):
    try:
        skills = Skill.objects.all()
        skills_list = ", ".join([skill.name for skill in skills])

        return render(request, 'answer.html', {'answer': skills_list})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def add_skill_to_vacancy(request):
    try:
        if request.method == 'POST':
            data = request.POST
            vacancy_id = data.get('vacancy')
            skill_id = data.get('skill')

            vacancy = Vacancy.objects.get(id=vacancy_id)
            skill = Skill.objects.get(id=skill_id)

            VacancySkill.objects.create(vacancy=vacancy, skill=skill)

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def add_skill_to_user(request):
    try:
        if request.method == 'POST':
            data = request.POST
            user_id = data.get('user')
            skill_id = data.get('skill')

            user = MyUser .objects.get(id=user_id)
            skill = Skill.objects.get(id=skill_id)

            UserSkill.objects.create(user=user, skill=skill)

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def remove_skill_from_user(request):
    try:
        if request.method == 'POST':
            data = request.POST
            user_id = data.get('user')
            skill_id = data.get('skill')

            user = MyUser .objects.get(id=user_id)
            skill = Skill.objects.get(id=skill_id)

            UserSkill.objects.get(user=user, skill=skill).delete()

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def remove_skill_from_vacancy(request):
    try:
        if request.method == 'POST':
            data = request.POST
            vacancy_id = data.get('vacancy')
            skill_id = data.get('skill')

            vacancy = Vacancy.objects.get(id=vacancy_id)
            skill = Skill.objects.get(id=skill_id)

            VacancySkill.objects.get(vacancy=vacancy, skill=skill).delete()

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def add_response(request):
    try:
        if request.method == 'POST':
            data = request.POST
            user_id = data.get('user')
            vacancy_id = data.get('vacancy')
            message = data.get('message')

            user = MyUser .objects.get(id=user_id)
            vacancy = Vacancy.objects.get(id=vacancy_id)

            user_response = UserResponse(user=user, vacancy=vacancy, message=message)
            user_response.save()

            return render(request, 'answer.html', {'answer': user_response.id})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def get_response(request):
    try:
        if request.method == 'GET':
            response_id = request.GET.get('id')
            user_response = UserResponse.objects.get(id=response_id)

            return render(request, 'answer.html', {'answer': user_response.message})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


@csrf_exempt
def delete_response(request):
    try:
        if request.method == 'POST':
            response_id = request.POST.get('id')
            UserResponse.objects.get(id=response_id).delete()

            return render(request, 'answer.html', {'answer': True})
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})