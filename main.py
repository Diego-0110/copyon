from typing import Callable
import copykitten
import argparse
from config import readConfig, Config
import threading
import os
import shutil
import consts


class ClipboardManager:
    def __init__(self, process: Callable):
        # Semaphore to warn that the user wants to close the app
        # value=0 to wake up thread on release
        self.close_sem = threading.Semaphore(value=0)
        # Function that process the content in the clipboard
        self.process = process

    def thread_exit(self):
        # Let the user exit safely
        while True:
            str_in = input()
            if (str_in == 'q' or str_in == 'quit'):
                # Warn the other thread to close
                self.close_sem.release()
                break

    def get_curr_clipboard(self):
        # copykitten.paste() may raise an error when the clipboard is empty
        try:
            return copykitten.paste()
        except Exception:
            return None

    # TODO: add image clipboard
    def thread_clipboard(self):
        curr_value = self.get_curr_clipboard()
        close = False
        # TODO: listen event of clipboard change instead of sleep 0.2s
        while not close:
            new_value = self.get_curr_clipboard()
            # clipboard has changed and has a valid value
            if curr_value != new_value and new_value is not None:
                processed_value = self.process(new_value)
                # Add the processed value to the clipboard
                copykitten.copy(processed_value)
                curr_value = processed_value
            # Wait until other thread call release or passes 0.2s
            # only when the release method is called return True
            close = self.close_sem.acquire(timeout=0.2)

    def run(self):
        th_exit = threading.Thread(target=self.thread_exit)
        th_clip = threading.Thread(target=self.thread_clipboard)
        th_exit.start()
        th_clip.start()
        # Wait until all threads finish
        th_exit.join()
        th_clip.join()


def copy_default_file(filename: str):
    dest_file = os.path.join(consts.CONFIG_COPYON, filename)
    # Create directories if not exists for the config directory
    if not os.path.exists(consts.CONFIG_COPYON):
        os.mkdir(consts.CONFIG_COPYON)
    # Check file named 'filename' exists in config directory
    file_exists = os.path.isfile(dest_file)
    while file_exists:
        res = input(f'{filename} already exists, do you want to overwrite it (y/n)?')
        # Keep asking until the user answers with y/Y or n/N
        if res.lower() == 'n':
            print(f'{filename} overwrite canceled')
            return
        elif res.lower() == 'y':
            break

    # Get directory of this python file (avoid relativity)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # Get default file from lua/ directory
    src_file = os.path.join(curr_dir, f'lua/{filename}')
    # Copy src_file to dest_file
    shutil.copyfile(src_file, dest_file)
    print(f'{filename} added')


def main():
    # Define argument parser
    parser = argparse.ArgumentParser(
        prog="copyon",
        description="Transform the text you save in the clipboard",
        epilog=f'Config directory: $CONFIG_COPYON (current value: {consts.CONFIG_COPYON})',
    )
    # Define alowed options
    # -l -t -c don't need additional parameters, only are set to true when are present
    # -l -> args.list == true ...
    parser.add_argument('-l', '--list', action='store_true', help="List processors")
    parser.add_argument('-t', '--types', action='store_true',
                        help="Add a types.lua file in $HOME_COPYON with type annotations")
    parser.add_argument('-c', '--config', action='store_true',
                        help="Add a config.lua file in $HOME_COPYON with the default config")
    # processor_id can be one valid id from the processors defined in the config or undefined
    parser.add_argument('processor_id', nargs='?', default=None)

    args = parser.parse_args()

    # At least one option should be used
    if not any(vars(args).values()):
        print('You need to use one of the available options.')
        print('')
        parser.print_help()
        return

    # user use -l or pass a processor_id so the config needs to be loaded
    if args.list or args.processor_id:
        try:
            config: Config = readConfig()
        except Exception as e:
            print(f'Error while reading config: {repr(e)}')
            exit()

    # Handle options:

    if args.list:
        processors = config['processors']
        print('List of processors:')
        for p in processors:
            if p.get('desc'):
                print(f' - "{p['id']}": {p.get('desc') or ''}')
            else:
                print(f' - "{p['id']}"')

    if args.types:
        copy_default_file('types.lua')

    if args.config:
        copy_default_file('config.lua')

    if args.processor_id:
        processor = [p for p in config['processors'] if p['id'] == args.processor_id]
        if len(processor) == 0:
            print(f'Processor "{args.processor_id}" doesn\'t exist')
            return
        processor = processor[0]
        print(f'Processor "{processor['id']}" running... (exit with q or quit)')
        processor_func = processor['process']
        clip_manager = ClipboardManager(processor_func)
        clip_manager.run()


if __name__ == "__main__":
    main()

