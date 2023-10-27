import random
import base64
from datetime import datetime

def gerador_codigo_seguranca():
    codigo = random.randint(100000, 999999)
    return base64.b64encode(codigo.encode()).decode()

def obter_datatime():
    agora = datetime.now()
    formato = "%Y-%m-%d %H:%M:%S"
    data_e_hora_formatadas = agora.strftime(formato)
    return data_e_hora_formatadas


