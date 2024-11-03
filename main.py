from pymem import *
from pymem.process import *
from pymem.exception import *
import json

# É necessária usar a função builtin da função Open, para não entrar em conflito com a biblioteca pymem
with __builtins__.open("settings.json","r") as arquivo:
    data = json.load(arquivo)
    name = data["life"]["name"]
    # convertendo o arquivo carregado para hexadecimal usando o parametro int(arq, 16)
    endereco = int(data["life"]["endereco"],16)

    # criando um list comprehension para a conversão de todos as offsets para hexadecimal
    offsets = [int(f"0x{offset}", 16) for offset in data["life"]["offsets"]]


pm = Pymem("SkyrimSE.exe")
module = module_from_name(pm.process_handle,name).lpBaseOfDll


def getPointer(base, offsets):
    addr = pm.read_ulonglong(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = pm.read_ulonglong(addr + offset)
    addr += offsets[-1]
    return addr

while True:
    pm.write_float(getPointer(module + endereco, offsets),1000.0)
    print("Injetado")