
import os
import sys
import sqlalchemy
import paramiko
import socket

PY3 = sys.version_info[0] == 3
if PY3:
    import urllib.request
    import urllib.parse
    
    urlparse = urllib.parse.urlparse
    urlopen = urllib.request.urlopen
    fopen = open
    
else:
    import urllib
    import urlparse
    import io
    
    urlparse = urlparse.urlparse
    urlopen = urllib.urlopen
    fopen = io.open

DATABASE_SCHEME = sqlalchemy.dialects.__all__
LOCALE_FILE_SCHEME = ('file', '')
URL_SCHEME = ('http','https','ftp')
SSH_SCHEME = ('ssh')

class SSHOpener(object):
    def __init__(self, parsed_url, mode, use_ggs_api = False, do_ggs_api_key_exchange = False):
        self.use_ggs_api = use_ggs_api
        self.do_ggs_api_key_exchange = do_ggs_api_key_exchange
        self.path = parsed_url.path
        self.mode = mode
        self.port = 22
        self.username, self.hostname = parsed_url.netloc.split('@')
        self.username, self.password = self.username.split(':')
        if self.hostname.find(':') >= 0:
            self.hostname, portstr = self.hostname.split(':')
            self.port = int(portstr)
        
    def __enter__(self):
        hostkeytype = None
        hostkey = None
        
        try:
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                host_keys = {}

        if self.hostname in host_keys:
            hostkeytype = host_keys[self.hostname].keys()[0]
            hostkey = host_keys[self.hostname][hostkeytype]

        self.t = paramiko.Transport((self.hostname, self.port))
        self.t.connect(hostkey, self.username, self.password, gss_host = socket.getfqdn(self.hostname),
            gss_auth = self.use_ggs_api, gss_kex = self.do_ggs_api_key_exchange )
        self.sftp = paramiko.SFTPClient.from_transport(self.t)
        self.fp =  self.sftp.open(self.path, self.mode)
        return self.fp
        
    def __exit__(self, type, value, tb):
        self.fp.close()
        self.t.close()

class DatabaseOpener(object):
    def __init__(self, url):
        self.url = url
        
    def __enter__(self):
        self.engine = sqlalchemy.create_engine( self.url )
        self.db_connection = self.engine.connect()
        self.db_metadata = sqlalchemy.MetaData()
        self.db_metadata.bind = self.db_connection.engine
        return self.db_connection
        
    def __exit__(self, type, value, tb):
        self.db_connection.close()

class LocaleFileOpener(object):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.args = args
        self.kwargs = kwargs
        
    def __enter__(self):
        self.fd = fopen(self.path, *self.args, **self.kwargs)
        return self.fd
        
    def __exit__(self, type, value, tb):
        self.fd.close()
        
class URLOpener(object):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs
        
    def __enter__(self):
        self.response = urlopen(self.url, *self.args, **self.kwargs)
        return self.response
        
    def __exit__(self, type, value, tb):
        self.response.close()

class SchemeNotImplemented(RuntimeError):
    pass

class Open(object):
    def __new__(cls, uri, *args, **kwargs):        
        parsed_uri = urlparse(uri)
        
        if kwargs.get('opener') is not None:
            return kwargs.get('opener')(parsed_uri.path, *args, **kwargs)
            
        elif parsed_uri.scheme.lower() in DATABASE_SCHEME:
            return DatabaseOpener(uri)
        
        elif parsed_uri.scheme.lower() in LOCALE_FILE_SCHEME:
            return LocaleFileOpener(parsed_uri.path, *args, **kwargs)
            
        elif parsed_uri.scheme.lower() in URL_SCHEME:
            return URLOpener(uri)
            
        elif parsed_uri.scheme.lower() in SSH_SCHEME:
            return SSHOpener(parsed_uri, *args, **kwargs)
            
        raise SchemeNotImplemented()