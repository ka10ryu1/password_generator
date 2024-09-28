#!/usr/bin/env python3
# -*-coding: utf-8 -*-
import argparse
import secrets
from string import ascii_letters, digits


def command():
    parser = argparse.ArgumentParser(description='パスワード生成スクリプト')
    parser.add_argument(
        '-n',
        type=int,
        metavar='PASS_NUM',
        default=16,
        help='生成するパスワードの文字数 [default:%(default)s]',
    )
    parser.add_argument(
        '--no_symbol',
        action='store_true',
        help='記号を使用しないモード',
    )
    return parser.parse_args()


def _select_password(length, get_pass_chars):
    password = ''.join(secrets.choice(get_pass_chars) for _ in range(length))
    # フォントによっては肉眼での判別が難しいものがあるので、1種類に統一する
    return password.replace('I', '1').replace('l', '1').replace('i', '1').replace('o', '0').replace('O', '0')


def get_random_password_v1(length):
    return _select_password(length, ascii_letters + digits)


def get_random_password_v2(length):
    return _select_password(length, ascii_letters + digits + '@#$%&?!<>_-')


def main(args):
    print(args)
    print(f'{"_/" * (args.n // 2)}')

    if args.no_symbol:
        print(get_random_password_v1(args.n))
    else:
        print(get_random_password_v2(args.n))

    print(f'{"_/" * (args.n // 2)}')


if __name__ == '__main__':
    exit(main(command()))
