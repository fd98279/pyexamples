'''
Created on Aug 30, 2017

@author: admin
'''
from rackindexer import core
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='frontend.py', usage='%(prog)s [--data blob] [--directory full_directory_path] [--files comma_separted_full_file_paths] ')
    parser.add_argument('--data', metavar='blob', type=str, nargs='+',
                        help='String blob')
    parser.add_argument('--dir', metavar='directory', type=str, nargs='+',
                            help='full directory path')
    parser.add_argument('--files', metavar='files', type=str, nargs='+',
                            help='Comma separated filenames with full path')    
    args = parser.parse_args()
    
    parser = core.parser()
    if args.data:
        parser.parse_blob(args.data.pop())
    
    reporter = core.stats_reporter(parser)
    reporter.print_report()
