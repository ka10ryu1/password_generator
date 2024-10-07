#!/usr/bin/env python3
# -*-coding: utf-8 -*-
import secrets
from argparse import ArgumentParser, Namespace
from string import ascii_letters, digits
from pathlib import Path

from measure_time import time_it, get_file_name


def command():
    parser = ArgumentParser(description='パスワード生成スクリプト')
    parser.add_argument(
        '-n',
        type=int,
        metavar='PASS_NUM',
        default=16,
        help='生成するパスワードの文字数 [default:%(default)s]',
    )
    parser.add_argument(
        '--out',
        type=Path,
        default='out',
        metavar='PATH',
        help='パスワードの保存ディレクトリ [default:%(default)s]',
    )
    parser.add_argument(
        '--name',
        type=Path,
        default=None,
        metavar='PATH',
        help='パスワードを保存したい時のファイル名 [defaultは作成しない]',
    )
    parser.add_argument(
        '--no_symbol',
        action='store_true',
        help='記号を使用しないモード',
    )
    return parser.parse_args()


@time_it('mkdir')
def mkdir(path: Path):
    # 親ディレクトリが存在しない場合
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    # ファイルが指定されている場合（is_file()は存在しているファイルにしか反応しない）
    elif path.suffix:
        pass
    # ディレクトリが指定されている場合
    elif not path.exists():
        print(f'mkdir {path.as_posix()}')
        path.mkdir()

    return path


def _select_password(length: int, get_pass_chars: str):
    password = ''.join(secrets.choice(get_pass_chars) for _ in range(length))
    # フォントによっては肉眼での判別が難しいものがあるので、1種類に統一する
    return password.replace('I', '1').replace('l', '1').replace('i', '1').replace('o', '0').replace('O', '0')


@time_it('letter + digit')
def get_random_password_v1(length: int):
    return _select_password(length, ascii_letters + digits)


@time_it('letter + digit + symbol')
def get_random_password_v2(length: int):
    return _select_password(length, ascii_letters + digits + '@#$%&?!<>_-')


@time_it(get_file_name(__file__))
def main(args: Namespace):
    """
    指定された引数に基づいてランダムなパスワードを生成して表示する

    Args:
        args (Namespace): 次の属性を含む名前空間オブジェクト:
            - n (int): 生成するパスワードの長さ
            - no_symbol (bool): パスワードから記号を除外するかどうかを示すフラグ
    Returns:
        int: 常に0を返す
    """
    print(args)

    grp = get_random_password_v1 if args.no_symbol else get_random_password_v2
    passwd = grp(args.n)

    print(f'{"_/" * (args.n // 2 + 4)}')
    print(f'{passwd=:}')
    print(f'{"_/" * (args.n // 2 + 4)}')

    if args.name is not None:

        if not args.name.suffix:
            args.name = args.name.with_suffix('.txt')

        save_path = mkdir(args.out) / args.name
        with save_path.open('w') as f:
            f.write(passwd)

        print(f'write {save_path.as_posix()}')

    return 0


if __name__ == '__main__':
    exit(main(command()))
