# coding=utf-8


from os.path import abspath, dirname, join

from django.db.models import Q

from minicup_administration.conf import configure_django

configure_django()
from minicup_photo_classifier.utils.download_tag import TagDownloader

import logging

TRAIN_DIR = abspath(join(dirname(__file__), 'train'))
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    tag_downloader = TagDownloader(TRAIN_DIR)

    tag_downloader.download_by_filter(
        Q(slug__contains='tatran-litovel', year__slug='2017', team_info_tag__category__slug='mladsi'),
        photo_limit=120,
    )

    tag_downloader.download_by_filter(
        Q(year__slug='2017', team_info_tag__category__slug='mladsi') & ~Q(slug__contains='tatran-litovel'),
        target_dir='other',
        photo_limit=120,
    )
