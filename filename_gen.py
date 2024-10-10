#!/usr/bin/env python3
# -*-coding: utf-8 -*-
from argparse import ArgumentParser, Namespace

from measure_time import time_it, get_file_name
from passwd_gen import get_random_str_v1


def command():
    parser = ArgumentParser(description='ファイル名生成スクリプト')
    parser.add_argument(
        '-n',
        type=int,
        nargs='+',
        metavar='PASS_NUM',
        default=[8, 4, 4, 4, 12],
        help='生成するパスワードの文字数 [default:%(default)s]',
    )
    parser.add_argument(
        '--ext',
        metavar='EXT',
        default='png',
        choices=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', ''],
        help='付与する拡張子 [default:%(default)s]',
    )
    return parser.parse_args()


@time_it(get_file_name(__file__))
def main(args: Namespace):
    """
    メイン関数は、提供された引数に基づいてランダムな文字列を生成し、出力する

    Args:
        args (Namespace): 引数を含む名前空間オブジェクト

    Returns:
        int: 常に0を返す
    """

    print(args)
    ext = f'.{args.ext}' if args.ext else args.ext
    print(f"{'-'.join([get_random_str_v1(n) for n in args.n])}{ext}")
    return 0


if __name__ == '__main__':
    exit(main(command()))
