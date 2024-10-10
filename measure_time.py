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


### ここから先の処理は、このスクリプトが直接呼ばれた場合のみ実行される
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


def _get_exec_name(line: str):
    return line.split('[')[-1].replace(']', '')


def _get_exec_pos(line: str, check_marker: str = '<'):
    return line.find(check_marker)


def _search_log(
    input_lines: list[str], check_exec: str = '<< exec start', space_num: int = 4
):
    """
    入力行のリストを処理して、実行ブロックを識別しフォーマットする

    Args:
        input_lines (list of str): 処理する入力行
        check_exec (str, optional): 実行ブロックの開始を識別するマーカ文字列
        space_num (int, optional): 実行ブロック内の行の先頭に追加するスペースの数

    Returns:
        tuple: 次の要素を含むタプル:
        - bool: 入力行が変更されていない場合はTrue、それ以外の場合はFalse
        - list of str: 実行ブロックがフォーマットされた処理済みの行
    """
    old_line = ''
    continue_flag = False
    exec_name = ''
    new_lines = []
    for line in input_lines:
        # デバッグ用
        # print(f'{continue_flag=},{exec_name=},{_get_exec_pos(old_line):2},{_get_exec_pos(line):2}')
        """
        今の行と前の行が同じ実行ブロック（check_exec） かつ
        実行ブロックの開始マーカ（check_marker）の位置が同じ かつ
        exec_nameが空文字の場合にインデント下げを行い、exec_nameを取得し、continue_flagをセット

        再度、同じexec_nameが登場した場合はインデントを戻し、exec_nameを空文字にして、continue_flagをリセット

        continue_flagがTrueの場合はインデント下げを継続

        それ以外の場合はそのままの行を追加
        """
        if (
            check_exec in old_line
            and check_exec in line
            and _get_exec_pos(old_line) == _get_exec_pos(line)
            and exec_name == ''
        ):
            new_lines.append(' ' * space_num + line)
            exec_name = _get_exec_name(old_line)
            continue_flag = True

        elif _get_exec_name(line) == exec_name:
            new_lines.append(line)
            exec_name = ''
            continue_flag = False

        elif continue_flag:
            new_lines.append(' ' * space_num + line)

        else:
            new_lines.append(line)

        old_line = line

    return input_lines == new_lines, new_lines


def _main(args: Namespace):
    if not args.input_log_txt.exists():
        print(f'指定されたファイルが存在しません: {args.input_log_txt}')
        exit(1)

    with args.input_log_txt.open() as fp:
        lines = [line.rstrip('\n') for line in fp]

    N = 10
    for i in range(N):
        """
        インデント下げは一度にまとめて実施しないで、順を追って実追って実施する
        そのため、N回繰り返しても変更がない場合は処理を終了する
        """
        flg, lines = _search_log(lines)
        # デバッグ用
        # print(f'### {i} ###')
        # for j in lines:
        #     print(j)

        if flg:
            break

    print(f'試行回数: {i}')

    # 上書きの場合は入力パスをそのまま出力パスとして使用
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

### measure_time.pyが直接呼ばれていない場合は以下の処理が実行される
logger.debug(
    f'### Hello {__name__.upper()} Logger! [{dt.now().strftime("%y.%m.%d %H:%M:%S")}] ###'
)
