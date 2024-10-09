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
    return parser.parse_args()


@time_it(get_file_name(__file__))
def main(args: Namespace):
    """
    ランダムなファイル名を生成する

    Args:
        args (Namespace): 引数を含む名前空間オブジェクト
            'n' という属性を持ち、各パスワードの長さを表す整数のリストであること
    Returns:
        int: 常に0を返す
    """

    print(args)
    print('-'.join([get_random_str_v1(n) for n in args.n]))
    return 0


if __name__ == '__main__':
    exit(main(command()))
