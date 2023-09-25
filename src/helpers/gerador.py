import random
import base64

def gerador_codigo_seguranca():
    codigo = random.randint(100000, 999999)
    return base64.b64encode(codigo.encode()).decode()
