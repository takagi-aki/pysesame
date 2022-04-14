from pysesame import Sesame

import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Operate sesame by console.')
parser.add_argument('command',
                    choices=['init', 'lock', 'unlock',
                             'toggle', 'get_log', 'get_status'],
                    help='Type of command that send to Sesame4.')
parser.add_argument('--file', '-f', nargs='?',
                    help='Path of JSON file, that has uuid and some keys.')
parser.add_argument('--page', nargs='?',
                    help='It use with "get_log" command. Specify log page.')
parser.add_argument('--lg', nargs='?',
                    help='It use with "get_log" command. Specify size of log.')

args = parser.parse_args()

if args.command == 'init':
    shutil.copy('pysesame/sample.json', './pysesame_key.json')
    exit()

if args.file:
    file_path = args.file
else:
    file_path = './pysesame_key.json'

if not os.path.exists(file_path):
    print('File not found!')
    exit()

my_sesame = Sesame(file_path=file_path)

if args.command == 'lock':
    my_sesame.lock()
elif args.command == 'unlock':
    my_sesame.unlock()
elif args.command == 'toggle':
    my_sesame.toggle()
elif args.command == 'get_log':
    dicarg = dict()
    if args.page:
        dicarg['page'] = args.page
    if args.lg:
        dicarg['lg'] = args.lg
    my_sesame.get_log(**dicarg)
elif(args.command == 'get_status'):
    my_sesame.get_status()
