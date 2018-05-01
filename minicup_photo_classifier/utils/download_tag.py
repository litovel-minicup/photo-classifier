# coding=utf-8
import logging
import os
from glob import glob
from multiprocessing.pool import Pool
from os import mkdir
from os.path import exists, join, basename

from PIL import Image
from builtins import map
from paramiko import SSHClient, SSHConfig, client
from scp import SCPClient

from minicup_administration.core.models import Tag

logger = logging.getLogger(__name__)


class TagDownloader(object):
    REMOTE_MEDIA_PATH = '/var/www/html/minicup.cz/shared/www/media/_original'

    def __init__(self, output_dir: str):
        assert exists(output_dir), "Output dir {} does not exist.".format(output_dir)
        self._output_dir = output_dir

        ssh_config = SSHConfig()
        user_config_file = os.path.expanduser("~/.ssh/config")
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                ssh_config.parse(f)

        self._ssh_client = SSHClient()

        self._ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        # self._ssh_client.

        self._ssh_config = ssh_config.lookup('minicup')

        self._ssh_client.load_system_host_keys()
        self._ssh_config = {
            "hostname": self._ssh_config["hostname"],
            "username": self._ssh_config["user"],
            # "port": int(self._ssh_config["port"]),
            'key_filename': self._ssh_config['identityfile']
        }
        self._ssh_client.connect(**self._ssh_config)

    def download_tag(self, tag: Tag, target_dir=None, photo_limit=None):
        logger.info('Downloading tag {} into {}.'.format(tag.slug, target_dir or tag.slug))
        target_dir = join(self._output_dir, target_dir or tag.slug)
        try:
            mkdir(target_dir)
        except FileExistsError:
            pass

        photos = set(p.photo.filename for p in tag.photo_tag_tag.all()[:photo_limit])

        already_downloaded = set(map(basename, glob('{}/*'.format(target_dir))))

        def progress(filename, size, sent):
            if (sent == size):
                print('{} {:.0f}'.format(filename, 100 * (sent / float(size))))

        to_download = photos - already_downloaded
        if not to_download:
            return

        with SCPClient(self._ssh_client.get_transport(), progress=progress) as scp:
            for p in to_download:
                logger.info('Downloading {} start.'.format(p))
                scp.get(
                    remote_path='{}/{}'.format(
                        self.REMOTE_MEDIA_PATH.rstrip('/'),
                        p
                    ),
                    local_path=target_dir
                )
                logger.info('Downloading {} done.'.format(p))

    def download_by_filter(self, tag_filter, target_dir=None, photo_limit=None):
        tags = Tag.objects.filter(tag_filter)
        logger.info('Downloading {} tags.'.format(tags.count()))
        for tag in tags:
            self.download_tag(tag, target_dir=target_dir, photo_limit=photo_limit)
