from pymem import *
from pymem.process import *
from pymem.exception import *
import json

with __builtins__.open("settings.json","r") as arquivo:
    data = json.load(arquivo)
    name = data["configs"]["name"]
    endereco = int(data["configs"]["endereco"],16)
    offsets = [int(f"0x{offset}", 16) for offset in data["configs"]["offsets"]]


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