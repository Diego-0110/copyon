import consts
from lupa.lua54 import LuaRuntime
from schema import Schema, Use, And, Optional, SchemaError
from utils import lua_function, lua_table_dict, lua_table_list, check_unique_field
from typing import Callable, TypedDict, NotRequired, List


# String used to test the process function from Processor
STR_TEST = 'abcdef abcdef ,.'
def check_process_func(func) -> Callable:
    """Check func is a Lua function that returns str"""
    lua_function(func)
    try:
        res = func(STR_TEST)
    except Exception:
        raise SchemaError('Error while calling function')
    if not isinstance(res, str):
        raise SchemaError('Function doesn\'t return string')
    return func


class Processor(TypedDict):
    id: str
    process: Callable
    desc: NotRequired[str]


class Config(TypedDict):
    processors: List[Processor]


CONFIG_SCHEMA = Schema(And(Use(lua_table_dict), {
    "processors": And(Use(lua_table_list), [
        And(Use(lua_table_dict), {
            "id": str,
            "process": Use(check_process_func),
            Optional("desc"): str
        })
    ], lambda d: check_unique_field(d, "id"))
}))


def readConfig() -> Config:
    lua = LuaRuntime()

    try:
        config_content = open(f'{consts.CONFIG_COPYON}/config.lua').read()
        config_table = lua.execute(config_content)
        return CONFIG_SCHEMA.validate(config_table)
    except OSError:
        raise Exception('Error loading config file')
    except SchemaError:
        raise Exception(f'Error validating config')

