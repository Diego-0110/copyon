# CoPyon

A configurable util to transform the copied text in the clipboard.

Define the processors with a Lua config file (config.lua):
```lua
---@type Config
return {
    processors = {
        {
            id = "upper",
            process = function (str_in)
                return string.upper(str_in)
            end,
            desc = "Convert all letters to uppercase"
        },
        -- ...
    }
}
```

Use a processor passing its `id` to the app:
```
python main.py upper
```

Now, every time you copy something in the clipboard, the function `process` will be called:
```
You copy:
"In a village in la Mancha, whose name I do not care to remember"

The app will add this to the clipboard:
"IN A VILLAGE IN LA MANCHA, WHOSE NAME I DO NOT CARE TO REMEMBER"
```

## Installation

Create a new virtual environment inside the root folder:
```
python -m venv .venv
```

Install the dependencies:
```
pip install -r requirements.txt
```

## Manual

```
usage: copyon [-h] [-l] [-t] [-c] [processor_id]

Transform the text you save in the clipboard

positional arguments:
  processor_id

options:
  -h, --help    show this help message and exit
  -l, --list    List processors
  -t, --types   Add a types.lua file in $CONFIG_COPYON with type annotations
  -c, --config  Add a config.lua file in $CONFIG_COPYON with the default config

Config directory: $CONFIG_COPYON (current value: ...)
```

## Usage

To be useful the app needs a defined configuration. You can get a default configuration (config.lua) with types (types.lua), using:
```
python main.py -tc
```

>Note: the configuration directory is defined by the environment variable `$CONFIG_COPYON` which default value is `$HOME/.config/copyon` (Linux)

After adding the default configuration you can edit it (config.lua) to add more processors:
```lua
---@type Config
return {
    processors = {
        -- ...
        {
            id = "new_processor",
            process = function (str_in)
                -- Do something with str_in
                -- return transformed str_in
            end,
            desc = "Description..." -- optional
        },
        -- ...
    }
}
```

Then consult the list of processors updated with:
```
> python main.py -l
List of processors:
 - "upper": Convert all letters to uppercase
 - "lower": Convert all letters to lowercase
 - "reverse": Invert the text
 - "new_processor": Description...
```

Run the new processor with:
```
python main.py new_processor
```
>You can stop the app entering `q` or `quit`.

