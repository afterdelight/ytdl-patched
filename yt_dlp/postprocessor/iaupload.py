from __future__ import unicode_literals

import subprocess

from .exec import ExecPP
from ..options import instantiate_parser
from ..utils import (
    encodeArgument,
    PostProcessingError,
)

iaup_options = instantiate_parser()
iaup_options.set_usage('[OPTIONS] IDENTIFIER FILE [FILE...]')

iaup_options.add_option(
    '-q', '--quiet',
    action='store_true', dest='quiet',
    help='Runs without output. Isolated from --quiet option from the outside')
iaup_options.add_option(
    '-d', '--debug',
    action='store_true', dest='debug',
    help='Runs in debug mode')

iaup_options.add_option(
    '-r', '--remote-name',
    metavar='PATH', dest='debug',
    help='Path to remote directory or filename')
iaup_options.add_option(
    '-m', '--metadata',
    metavar='K:V', dest='debug',
    help='Metadata to add')
iaup_options.add_option(
    '-H', '--header',
    metavar='K:V', dest='debug',
    help='Header to add')
iaup_options.add_option(
    '-D', '--derive',
    action='store_true', dest='debug', default=False,
    help='Enables "derive" task on IA. derive task is not enabled by default')
iaup_options.add_option(
    '-n', '--no-derive',
    action='store_false', dest='debug', default=False,
    help='Disables "derive" task on IA.')
iaup_options.add_option(
    '-R', '--retries',
    metavar='RETRIES', dest='debug', default=10000,
    type=int, help='Number of retries on SlowDown or connection being disconnected.')
iaup_options.add_option(
    '-t', '--throttled-rate',
    metavar='RATE', dest='debug', type=int,
    help=('Same as the option with same name on yt-dlp, but for upload in this time. '
          'Downloaded failure caused by this option will count for -R retries.'))
iaup_options.add_option(
    '-D', '--delete',
    action='store_true', dest='debug', default=False,
    help='Deletes files after all files are successfully uploaded.')
iaup_options.add_option(
    '-C', '--conflict-resolve',
    metavar='KIND:BEHAVIOR', dest='debug',
    help=('Specifies how to avoid/torelate errors while uploading. '
          'Allowed values for KIND are: size_overflow, no_perm. '
          'Allowed values for BEHAVIOR are: rename_ident, error, skip.'))


class InternetArchiveUploadPP(ExecPP):
    # memo
    #  This item total number of bytes(666) is over the per item size limit of 1099511627776. Please contact info@archive.org for help fitting your data into the archive.
    def run(self, info):
        for tmpl in self.exec_cmd:
            cmd = self.parse_cmd(tmpl, info)
            self.to_screen('Executing command: %s' % cmd)
            retCode = subprocess.call(encodeArgument(cmd), shell=True)
            if retCode != 0:
                raise PostProcessingError('Command returned error code %d' % retCode)
        return [], info
