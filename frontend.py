'''
Created on Aug 30, 2017

@author: admin
'''
from rackindexer import core
import argparse
import logging.config
import os.path
print(os.path.dirname(__file__))
LOGGING_CONF=os.path.join(os.path.dirname(__file__),
                          "logging_config.ini")
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='frontend.py', usage='%(prog)s [--data blob] [--directory full_directory_path] [--files comma_separted_full_file_paths] ')
    parser.add_argument('--data', metavar='blob', type=str, nargs='+',
                        help='String blob')
    parser.add_argument('--dir', metavar='directory', type=str, nargs='+',
                            help='full directory path')
    parser.add_argument('--files', metavar='files', type=str, nargs='+',
                            help='Comma separated filenames with full path')    
    args = parser.parse_args()
    
    parser = core.parser(logger)
    if args.data:
        parser.parse_blob(args.data.pop())
    
    reporter = core.stats_reporter(parser)
    reporter.print_report()
