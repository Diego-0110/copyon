from lupa.lua54 import lua_type
from schema import SchemaError


def lua_table_dict(table):
    if lua_type(table) == 'table':
        return dict(table)
    raise SchemaError()


def lua_table_list(table):
    if lua_type(table) == 'table':
        return list(table.values())
    raise SchemaError()


def lua_function(func):
    if lua_type(func) == 'function':
        return func
    raise SchemaError()


def check_unique_field(dict_list: list, fieldname: str):
    # Check in a list of dicts if the values of a field are unique
    return len(dict_list) == len(set(x[fieldname] for x in dict_list))
