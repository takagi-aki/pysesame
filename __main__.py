from pysesami import Sesami

import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('command', choices=['init', 'lock', 'unlock', 'toggle',
                    'get_log', 'get_status'], help='sum the integers (default: find the max)')
parser.add_argument('--file', '-f', nargs='?',
                    help='sum the integers (default: find the max)')
args = parser.parse_args()

if args.command == 'init':
    shutil.copy('pysesami/sample.json', './pysesami_key.json')
    exit()

if args.file:
    file_path = args.file
else:
    file_path = './pysesami_key.json'

print(file_path)

if not os.path.exists(file_path):
    print('File not found!')
    exit()

my_sesami = Sesami(file_path=file_path)

if args.command == 'lock':
    my_sesami.lock()
elif args.command == 'unlock':
    my_sesami.unlock()
elif args.command == 'toggle':
    my_sesami.toggle()
elif args.command == 'get_log':
    my_sesami.get_log()
elif(args.command == 'get_status'):
    my_sesami.get_status()
