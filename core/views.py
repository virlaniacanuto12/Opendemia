from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .models import DadosDemograficos, Relatorios, LocaisVisitados, Usuarios, Doencas, Cruzamento
import json
# Create your views here.

# Ler todos os estados da tabela de dados demográficos e relaciona com a quantidade de casos dos estados
def geochart(request):
    doencas = Doencas.objects.all()
    relatorios = Relatorios.objects.all()

    dselecionada = 0
    if (request.method == 'POST'):
            dselecionada = request.POST.get('doencas' , 0)
            print(dselecionada)

    relatorioPorDoenca = []
    for n in relatorios:
        if(n.doenca.id == int(dselecionada)):
            auxRelatorios = model_to_dict(n)
            relatorioPorDoenca.append(auxRelatorios)

    casosPorEstado = {}
    todosDadosDemograficos = DadosDemograficos.objects.all()
    for dadoDemografico in todosDadosDemograficos:
        casosPorEstado[dadoDemografico.estado] = 0

    for relatorio in relatorioPorDoenca:
        estado = DadosDemograficos.objects.get(pk=relatorio['dadosdemograficos']).estado
        casosPorEstado[estado] = relatorio['casos']

    casosPorEstadoList = []
    for key in casosPorEstado:
        casosPorEstadoList.append([key, casosPorEstado[key]])

    print(casosPorEstadoList)

    return render(request, 'index.html', {'auxpython': casosPorEstadoList, 'doencass': doencas})

def geochart2(request):
    doencas = Doencas.objects.all()
    relatorios = Relatorios.objects.all()

    dselecionada = 0
    if (request.method == 'POST'):
            data = json.loads(request.body.decode('utf-8'))
            dselecionada = int(data['value'])
            print(dselecionada)

    relatorioPorDoenca = []
    for n in relatorios:
        if(n.doenca.id == dselecionada):
            auxRelatorios = model_to_dict(n)
            relatorioPorDoenca.append(auxRelatorios)

    casosPorEstado = {}
    todosDadosDemograficos = DadosDemograficos.objects.all()
    for dadoDemografico in todosDadosDemograficos:
        casosPorEstado[dadoDemografico.estado] = 0

    for relatorio in relatorioPorDoenca:
        estado = DadosDemograficos.objects.get(pk=relatorio['dadosdemograficos']).estado
        casosPorEstado[estado] = relatorio['casos']

    casosPorEstadoList = []
    for key in casosPorEstado:
        casosPorEstadoList.append([key, casosPorEstado[key]])

    print(casosPorEstadoList)

    return render(request, 'index2.html', {'auxpython': casosPorEstadoList, 'doencass': doencas})


#Pegando os amigos dos usuários logados e registrando no banco
def submit_geochart(request):
        usuarios = Usuarios.objects.all()
        doencas = Doencas.objects.all()
        usuariosFinais = []
        for n in usuarios:
            user = model_to_dict(n)
            user.pop('locaisvisitados')
            usuariosFinais.append(user)

        usuario_nosso = Usuarios.objects.get(id_facebook =request.session["id_facebook"]) #Usuário que está logado
        cruzamento = Cruzamento.objects.filter(usuario_id = usuario_nosso.id) #Pegando id do usuário logado para pegar as doenças que ele registrou
        doencas_preparadas = []
        for c in cruzamento:
            aux = Doencas.objects.get(id = c.doenca_id.id)
            doencas_preparadas.append({"nome_doenca": aux.nome, "status": c.status, "id": aux.id})

        cruzamentoaux = Cruzamento.objects.all()
        cruzamentoNovo = []
        for c in cruzamentoaux:
            caux = model_to_dict(c)
            cruzamentoNovo.append(caux)

        return render(request, 'tela2.html', {'usuarioss': usuariosFinais, 'doencass': doencas, 'cruzamentos': cruzamento, 'nome_doencas': doencas_preparadas, 'crNovo': json.dumps(cruzamentoNovo)})


def registrarUsuario(request):
        if (request.method == 'POST'):
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            nome = data['nomeUsuario']
            id_facebook = data['idUsuario']
            idade = data['idadeUsuario']
            cidade = data['cidadeUsuario']

            novoUsuario = Usuarios.objects.create(nome = nome, id_facebook = id_facebook, idade = idade, cidade = cidade)
            request.session['id_facebook'] = novoUsuario.id
            print(request.session['id_facebook'])

            # Criando as linhas de um novo usuário na tabela de cruzamento
            doencas = Doencas.objects.all()
            for d in doencas:
                Cruzamento.objects.create(usuario_id = novoUsuario.id, doenca_id = d.id)

        return redirect('index/tela2')

def update_session(request, id_facebook_p):
    request.session['id_facebook'] = id_facebook_p
    print(id_facebook_p)
    print(request.session['id_facebook'])

    return redirect('/index/tela2')

def registrarCruzamento(request):
    if (request.method == 'POST'):
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            dataaux = data['listaStatus']
            aux2 = 0
        
            usuario_nosso = Usuarios.objects.get(id_facebook =request.session["id_facebook"]) #Usuário que está logado
            cruzamento = Cruzamento.objects.filter(usuario_id = usuario_nosso.id) #Pegando id do usuário logado para pegar as doenças que ele registrou
            for c in cruzamento:
                c.status = dataaux[aux2]
                c.save()
                aux2 = aux2 + 1

    return redirect('index/tela2')

#Pegando os locais visitados pelos usuários e registrando no banco
def guardarLocais(request):
        if (request.method == 'POST'):
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            cep = data['cep']
            cidade = data['cidade']
            estado = data['estado']
            pais = data['pais']
            latitude = data['latitude']
            longitude = data['longitude']

            LocaisVisitados.objects.create(cidade = cidade, estado = estado, pais = pais, latitude = latitude, longitude = longitude, cep = cep)

        return redirect('index/tela2')