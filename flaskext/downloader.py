# -*- coding: utf-8 -*-
"""
    flaskext.downloader
    ~~~~~~~~~~~~~~~~~~~

    Allow a Flask web app to download files on behalf of the user.

    :copyright: (c) 2011 by Kai Blin.
    :license: BSD, see LICENSE for more details.
"""
import urllib
import os.path
from werkzeug import FileStorage

class Downloader(object):
    """Download manager class for handling downloads in Flask
    """

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Set up this instance for use with *app*
        """
        self.app = app

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['downloader'] = self

        app.config.setdefault('DEFAULT_DOWNLOAD_DIR', os.path.dirname(__file__))

    def download(self, url):
        """Download the URL's contents, returning a :class:`FileStorage` instance

        If the URL cannot be opened, returns `None`
        """
        try:
            handle = urllib.urlopen(url)
            content_type = handle.headers.get('content-type',
                                'application/octet-stream')
            content_length = handle.headers.get('content-length', -1)
            store = FileStorage(stream=handle, content_type=content_type,
                                content_length=content_length,
                                headers=handle.headers)
            return store
        except IOError:
            return None

