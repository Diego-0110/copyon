import consts
from lupa.lua54 import LuaRuntime
from schema import Schema, Use, And, Optional, SchemaError
from utils import lua_function, lua_table_dict, lua_table_list, check_unique_field


STR_TEST = 'abcdef abcdef ,.'


def check_process_func(func):
    lua_function(func)
    try:
        res = func(STR_TEST)
        return func
    except Exception:
        raise SchemaError()
    if not isinstance(res, str):
        raise SchemaError()


CONFIG_SCHEMA = Schema(And(Use(lua_table_dict), {
    "processors": And(Use(lua_table_list), [
        And(Use(lua_table_dict), {
            "id": str,
            "process": Use(check_process_func),
            Optional("desc"): str
        })
    ], lambda d: check_unique_field(d, "id"))
}))


def readConfig():
    lua = LuaRuntime(unpack_returned_tuples=True)

    try:
        config_content = open(f'{consts.CONFIG_COPYON}/config.lua').read()
        config_table = lua.execute(config_content)
        return CONFIG_SCHEMA.validate(config_table)
    except OSError:
        raise Exception('Error loading config file')
    except SchemaError as e:
        raise Exception(f'Error validating config {repr(e)}')

