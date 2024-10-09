#!/usr/bin/env python3
# -*-coding: utf-8 -*-
from functools import wraps
from time import perf_counter
from pathlib import Path
from datetime import datetime as dt

from logging import getLogger, StreamHandler, FileHandler
from logging import DEBUG as log_DEBUG
from logging import INFO as log_INFO

# 計測時間を可視化したい時はDEBUG、そうでない時はINFOに設定
DEBUG_LV = log_INFO
DEBUG_LV = log_DEBUG
# 計測結果を標準出力したい場合はDEBUG_PATHを空文字に、ファイルに出力したい場合はファイルパスを指定
DEBUG_PATH = ''
DEBUG_PATH = 'log_time_it.txt'

logger = getLogger(__name__)
handler = FileHandler(DEBUG_PATH, mode='a') if DEBUG_PATH else StreamHandler()
handler.setLevel(DEBUG_LV)
logger.setLevel(DEBUG_LV)
logger.addHandler(handler)
logger.propagate = False


def get_file_name(file_name: str):
    return Path(file_name).stem


def time_it(pattern: str = '', get_time: bool = False):

    def _timer(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):
            st = perf_counter()

            if pattern:
                logger.debug(f'<< exec start [{pattern}]')

            out = func(*args, **kwargs)

            msg = '>> '
            if (now := perf_counter() - st) < 1:
                msg += f'{now * 1000:7.3f} ms'
            elif now < 180:
                msg += f'{now:8.4f} s'
            elif now < 180 * 60:
                msg += f'{now / 60:6.2f} min ({int(now)} s)'
            else:
                msg += f'{now / 3600:6.2f} h ({int(now)} s)'

            if pattern:
                msg += f' [{pattern}]'

            logger.debug(msg)

            return (now * 1000, out) if get_time else out

        return _wrapper

    return _timer

from argparse import ArgumentParser, Namespace

def _command():
    parser = ArgumentParser(description='パスワード生成スクリプト')
    parser.add_argument(
        'input_log_txt',
        type=Path,
        metavar='PATH',
        help='解析したいログのパス',
    )
    parser.add_argument(
        '--out_dir',
        type=Path,
        default='out',
        metavar='PATH',
        help='解析したログの保存ディレクトリ [default:%(default)s]',
    )    
    parser.add_argument(
        '--out_path',
        type=Path,
        default='log_analyzed.txt',
        metavar='PATH',
        help='解析したログのファイル名 [default:%(default)s]',
    )    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='入力パスをそのまま出力パスとして使用する上書きモード',
    )    
    return parser.parse_args()

def _get_exec_name(line:str):
    return line.split('[')[-1].replace(']','')

def _get_exec_pos(line:str):
    return line.find('<')

def _search_log(lines,check_exec:str = '<< exec start',space_num:int = 4):
    old_line = ''
    continue_flag = False
    exec_name = ''
    new_lines = []
    for line in lines:
        # print(0,line,old_line,continue_flag,exec_name)
        if check_exec in old_line and check_exec in line and _get_exec_pos(old_line) == _get_exec_pos(line):
            exec_name = _get_exec_name(old_line)
            new_lines.append(' ' * space_num +line)
            continue_flag = True
        elif _get_exec_name(line) == exec_name:
            continue_flag = False
            new_lines.append(line)
        elif continue_flag:
            new_lines.append(' ' * space_num +line)
        else:
            new_lines.append(line)

        old_line = line

    return exec_name == '',new_lines

def _main(args: Namespace):
    if not args.input_log_txt.exists():
        print(f'指定されたファイルが存在しません: {args.input_log_txt}')
        exit(1)

    with args.input_log_txt.open() as fp:
        lines = [line.rstrip('\n') for line in fp]

    for _ in range(10):
        flg,lines = _search_log(lines)
        if flg:
            break
        

    if args.overwrite:
        save_path = args.input_log_txt
    else:
        save_path = args.out_dir / args.out_path
        args.out_dir.mkdir(parents=True, exist_ok=True)

    with save_path.open('w') as fp:
        fp.write('\n'.join(lines) + '\n')

    return save_path.exists()


if __name__ == '__main__':
    exit(_main(_command()))

logger.debug(f'### Hello {__name__.upper()} Logger! [{dt.now().strftime('%y.%m.%d %H:%M:%S')}] ###')
