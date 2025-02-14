# CoPyon

A configurable util to transform the text copied in the clipboard.

## Installation

Create a new virtual environment inside the root folder:
```
python -m venv .venv
```

Install the dependencies:
```
pip install -r requirements.txt
```

## Usage

To be useful the app needs a defined configuration. You can get a default configuration with types, using:
```
python main.py -tc
```

>Note: the configuration directory is defined by the environment variable `\$CONFIG_COPYON` which default value is `\$HOME/.config/copyon`

After adding the default configuration you can run (to execute the processor 'upper'):
```
python main.py upper
```

Or consult the list of processors:
```
python main.py -l
```
