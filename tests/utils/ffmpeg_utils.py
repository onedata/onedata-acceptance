"""This module implements utility functions for management of ffmpeg.

Useful resources and tutorials used to create this module:
- How to capture desktop using ffmpeg: https://trac.ffmpeg.org/wiki/Capture/Desktop
- How to create mosaic out of several input videos: https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import time
import errno
from math import sqrt
import subprocess as sp
from itertools import chain, repeat
from contextlib import contextmanager


def start_recording(movie_dir, movie_name, displays, screen_width,
                    screen_height, mosaic_filter=True):
    if not os.path.exists(movie_dir):
        os.makedirs(movie_dir)

    cmd, paths = _create_ffmpeg_cmd(displays, screen_width, screen_height,
                                    movie_dir, movie_name, mosaic_filter)
    # remove old videos if they exist
    for path in paths:
        with _suppress(OSError, errnos=(errno.ENOENT, errno.ENAMETOOLONG)):
            os.remove(path)

    with open(os.devnull, 'w') as dev_null:
        proc = sp.Popen(cmd, stdin=sp.PIPE, stdout=dev_null,
                        stderr=dev_null, close_fds=True)

    # let ffmpeg start
    time.sleep(0.5)
    if proc.poll() is not None:
        raise RuntimeError('ffmpeg did not start')

    return proc, paths


def stop_recording(proc):
    with _suppress(IOError, errnos=(errno.EINVAL, errno.EPIPE)):
        proc.communicate(input=b'q')


# ============================================================================
# Internal functions
# ============================================================================


@contextmanager
def _suppress(exception, errnos):
    try:
        yield
    except exception as e:
        if errno and e.errno not in errnos:
            raise


def _create_ffmpeg_cmd(displays, width, height, dir_path, file_name,
                       mosaic_filter, qp=1):
    cmd = ['ffmpeg']

    wh = '{width}x{height}'.format(width=width, height=height)
    for display in displays:
        cmd.extend(['-framerate', '25', '-video_size', wh, '-f', 'x11grab',
                    '-i', '{display}'.format(display=display)])

    paths = []
    file_path = os.path.join(dir_path, file_name + '{}.mp4')
    output_fmt = ['-c:v', 'libx264', '-qp', str(qp), '-preset', 'ultrafast']

    display_num = len(displays)
    if display_num > 1:
        cmd.append('-filter_complex')
        if mosaic_filter:
            cmd.append(_create_mosaic_filter(displays, width, height))
        else:
            tagged_streams, tags = _tag_streams(display_num)
            cmd.append(tagged_streams)
            for tag in tags:
                tag = '[{tag}]'.format(tag=tag)
                path = file_path.format(tag)
                paths.append(path)
                cmd.extend(output_fmt + ['-map', tag, path])

    if display_num == 1 or mosaic_filter:
        path = file_path.format('')
        cmd.extend(output_fmt + [path])
        paths.append(path)

    return cmd, paths


def _create_mosaic_filter(displays, width, height):
    filter_fmt = 'nullsrc=size={width}x{height} [{base}]; {stream};{overlay}'
    available_screens = _gen_offsets(len(displays), width, height)
    full_width, full_height = next(available_screens)
    tagged_streams, tags = _tag_streams(len(displays))
    overlaid_streams, base = _overlay_streams(tags, available_screens)
    return filter_fmt.format(width=full_width, height=full_height,
                             base=base, stream=tagged_streams,
                             overlay=overlaid_streams)


def _overlay_streams(tags, offsets):
    overlay_fmt = '[{base}][{tag}] overlay=shortest=1:x={x}:y={y} [{new_base}]'
    last_overlay_fmt = '[{base}][{tag}] overlay=shortest=1:x={x}:y={y}'
    base_fmt = 'base{num}'

    formats = chain(repeat(overlay_fmt, len(tags) - 1), [last_overlay_fmt])
    bases = ((base_fmt.format(num=num), base_fmt.format(num=num+1))
             for num in xrange(len(tags)))
    offsets = iter(offsets)

    return (';'.join(fmt.format(base=base, tag=tag, x=x, y=y,
                                new_base=new_base)
                     for fmt, tag, (x, y), (base, new_base)
                     in zip(formats, tags, offsets, bases)),
            base_fmt.format(num=0))


def _tag_streams(input_streams_num):
    tags = ['v{num}'.format(num=num) for num in xrange(input_streams_num)]
    fmt = '[{stream}:v] setpts=PTS-STARTPTS [{tag}]'
    tagged_streams = ';'.join(fmt.format(stream=i, tag=tag)
                              for i, tag in enumerate(tags))
    return tagged_streams, tags


def _gen_offsets(screen_num, width, height):
    a = b = int(round(sqrt(screen_num)))
    if a*b < screen_num:
        a += 1
    yield int(a*width), int(b*height)
    for i in xrange(a):
        for j in xrange(b):
            yield int(i*width), int(j*height)
