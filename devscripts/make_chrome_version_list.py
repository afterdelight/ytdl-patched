# coding: utf-8
from __future__ import unicode_literals, print_function

import sys
import subprocess

sys.path[:0] = ['.']

from youtube_dl.utils import int_or_none


versions = set()

# https://stackoverflow.com/questions/10649814/get-last-git-tag-from-a-remote-repo-without-cloning
with subprocess.Popen(
        ['git', '-c', 'versionsort.suffix=-', 'ls-remote',
         '--tags', '--sort=v:refname', 'https://chromium.googlesource.com/chromium/src'],
        stdout=subprocess.PIPE,) as proc:
    for line in proc.stdout:
        commit_hash, tag_ref = line.strip().decode().split('\t')
        tag_name = tag_ref[10:]  # trim first "refs/tags/"
        version_tuple = tuple(int_or_none(x) for x in tag_name.split('.') if x.isdigit())
        if len(version_tuple) < 4:
            continue
        versions.add((version_tuple, tag_name))

versions = sorted(versions)
latest_version_major = versions[-1][0][0]
minimum_version = ((latest_version_major - 3, 0, 0, 0), '')  # automatically choose minimum

results = [x[1] for x in versions if x > minimum_version]

lf = '\n'
pycode = f'''# coding: utf-8
# AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
# Generated by ./devscripts/make_chrome_version_list.py
# This list is created from git tags in https://chromium.googlesource.com/chromium/src
from __future__ import unicode_literals

versions = [
{lf.join(f'    "{r}",' for r in sorted(results))}
]

__all__ = ['versions']
'''

with open('./youtube_dl/chrome_versions.py', 'w') as w:
    w.write(pycode)
