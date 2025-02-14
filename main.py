import copykitten
import time
import argparse
from config import readConfig
import threading
import os
import shutil
import consts


class ClipboardManager:
    def __init__(self, process):
        # TODO: use lock
        self.close = False
        self.process = process

    def thread_exit(self):
        while True:
            str_in = input('')
            if (str_in == 'q' or str_in == 'quit'):
                self.close = True
                break

    # TODO: add image clipboard
    def thread_clipboard(self):
        curr_value = copykitten.paste()
        while not self.close:
            new_value = copykitten.paste()
            # clipboard has changed
            if curr_value != new_value:
                processed_value = self.process(new_value)
                copykitten.copy(processed_value)
                curr_value = processed_value
            time.sleep(0.2)

    def run(self):
        th_exit = threading.Thread(target=self.thread_exit)
        th_clip = threading.Thread(target=self.thread_clipboard)
        th_exit.start()
        th_clip.start()
        th_exit.join()
        th_clip.join()


def copy_default_file(filename: str):
    dest_file = os.path.join(consts.CONFIG_COPYON, filename)
    if not os.path.exists(consts.CONFIG_COPYON):
        os.mkdir(consts.CONFIG_COPYON)
    file_exists = os.path.isfile(dest_file)
    ovewrite = True
    if file_exists:
        res = input(f'{filename} already exists, do you want to overwrite it (y/n)?')
        if res.lower() != 'y':
            ovewrite = False
            print(f'{filename} overwrite canceled')

    if ovewrite:
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        src_file = os.path.join(curr_dir, f'lua/{filename}')
        shutil.copyfile(src_file, dest_file)
        print(f'{filename} added')


def main():
    # Define argument parser
    parser = argparse.ArgumentParser(
        prog="CoPyon",
        description="Transform the text you save in the clipboard",
        add_help="CONFIG_COPYON (default: $HOME/.config/copyon)"
    )
    parser.add_argument('-l', '--list', action='store_true', help="List processors")
    parser.add_argument('-t', '--types', action='store_true',
                        help="Add a types.lua file in $HOME_COPYON with types annotations")
    parser.add_argument('-c', '--config', action='store_true',
                        help="Add a config.lua file in $HOME_COPYON with the default config")
    parser.add_argument('processor_id', nargs='?', default=None)

    args = parser.parse_args()

    if args.list or args.processor_id:
        try:
            config = readConfig()
        except Exception as e:
            print(f'Error while reading config: {repr(e)}')
            exit()

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
            print(f'Processor "{args.processor_id}" doesn\'t exists')
            return
        processor = processor[0]
        print(f'Processor "{processor['id']}" running... (exit with q or quit)')
        processor_func = processor['process']
        clip_manager = ClipboardManager(processor_func)
        clip_manager.run()


if __name__ == "__main__":
    main()

