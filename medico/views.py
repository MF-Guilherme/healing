from django.shortcuts import render, redirect
from .models import Especialidade, DadosMedico, is_medico, DatasAbertas
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime



def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é um médico cadastrado')
        return redirect('/medicos/abrir_horario')
    
    if request.method == 'GET':
        especialidades = Especialidade.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades})
    elif request.method == 'POST':
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

    dados_medico = DadosMedico(
        crm=crm,
        nome=nome,
        cep=cep,
        rua=rua,
        bairro=bairro,
        numero=numero,
        rg=rg,
        cedula_identidade_medica=cim,
        foto=foto,
        descricao=descricao,
        valor_consulta=valor_consulta,
        especialidade_id=especialidade,
        user = request.user
    )

    dados_medico.save()

    messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso!')
    return redirect('/medicos/abrir_horario')


def abrir_horario(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem abrir horários')
        return redirect('/usuarios/sair')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos})
    elif request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data não pode ser anterior a data atual')
            return redirect('/medicos/abrir_horario')
        
        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
            )
        
        horario_abrir.save()
        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso')
        return redirect('/medicos/abrir_horario')