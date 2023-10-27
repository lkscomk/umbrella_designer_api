from datetime import date, datetime

def validar_obrigatorio(dicionario, lista_itens):
    erros = []
    for item in lista_itens:
        if item not in dicionario or dicionario[item] is None or dicionario[item] == '':
            erros.append(f"{item} é obrigatório")
    if erros:
        return erros
    return True

def serializar_data(obj):
    if isinstance(obj, date):
        return obj.isoformat()

def verificar_maioridade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
    data_atual = datetime.now()
    idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
    print('aaaaa', type(idade))
    if idade < 18:
        return "O usuário deve ser maior de 18 anos."
    else:
        return True