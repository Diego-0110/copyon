from lupa.lua54 import lua_type
from schema import SchemaError
from typing import Any, Callable
import sys


# Lua utils for schema
def lua_table_dict(table: Any) -> dict[str, Any]:
    """Check table is a Lua table and returns it as a Python dict"""
    if lua_type(table) == 'table':
        return dict(table)
    raise SchemaError('Not a Lua table')


def lua_table_list(table: Any) -> list[Any]:
    """Check table is a Lua table and returns it as a Python list"""
    if lua_type(table) == 'table':
        return list(table.values())
    raise SchemaError('Not a Lua table')


def lua_function(func: Any) -> Callable:
    """Check func is a Lua function and returns it"""
    if lua_type(func) == 'function':
        return func
    raise SchemaError('Not a Lua function')

# Platform
def is_linux():
    return sys.platform.startswith('linux')

def is_macos():
    return sys.platform.startswith('darwin')

def is_windows():
    return sys.platform.startswith('win')


# Others
def check_unique_field(dict_list: list, fieldname: str) -> bool:
    """Check if the values of a field are unique in a list of dicts"""
    return len(dict_list) == len(set(x[fieldname] for x in dict_list))
