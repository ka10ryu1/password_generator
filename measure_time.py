#!/usr/bin/env python3
# -*-coding: utf-8 -*-
from functools import wraps
from time import perf_counter
from pathlib import Path

from logging import getLogger, StreamHandler, DEBUG, INFO

# 計測時間を可視化したい時はDEBUG、そうでない時はINFOに設定
DEBUG_LV = INFO
DEBUG_LV = DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG_LV)
logger.setLevel(DEBUG_LV)
logger.addHandler(handler)
logger.propagate = False
logger.debug(f'Hello {__name__.upper()} logger!')


def get_file_name(file_name: str):
    return Path(file_name).stem


def time_it(pattern: str = '', get_time: bool = False):

    def _timer(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):
            st = perf_counter()

            out = func(*args, **kwargs)

            msg = '>> '
            if (now := perf_counter() - st) < 1:
                msg += f'{now * 1000:7.3f} ms'
            elif now < 180:
                msg += f'{now:7.3f} s'
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
