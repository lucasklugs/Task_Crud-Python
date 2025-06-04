import decimal
import hashlib
import datetime

from typing import Any


# Função para converter a string para datetime
def parse_datetime(val):
    data_str = val.decode("utf-8")
    try:
        # Tenta converter considerando microssegundos
        return datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # Se falhar, tenta converter sem microssegundos
        return datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")