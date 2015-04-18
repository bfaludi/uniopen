
import sys
import sqlalchemy

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
URL_SCHEME = ('http','https')

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
    def __new__(cls, uri, opener = None, *args, **kwargs):        
        parsed_uri = urlparse(uri)
        
        if parsed_uri.scheme.lower() in DATABASE_SCHEME:
            return DatabaseOpener(uri)
        
        elif parsed_uri.scheme.lower() in LOCALE_FILE_SCHEME:
            return LocaleFileOpener(parsed_uri.path, *args, **kwargs)
            
        elif parsed_uri.scheme.lower() in URL_SCHEME:
            return URLOpener(uri)
            
        elif opener is not None:
            return opener(parsed_uri.path, *args, **kwargs)
            
        raise SchemeNotImplemented()