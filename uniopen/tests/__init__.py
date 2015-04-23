
import io
import os
import unittest
import uniopen
import smart_open

class Test_Opener( unittest.TestCase ):

    def test_locale_file_opener( self ):
        with uniopen.Open('uniopen/__init__.py', 'r', encoding = 'utf-8') as rs:
            self.assertIsNotNone(rs.read())

    def test_path_file_opener( self ):
        full_path = os.path.abspath('uniopen/__init__.py')
        with uniopen.Open( 'file://{}'.format(full_path), 'r', encoding = 'utf-8') as rs:
            self.assertIsNotNone(rs.read())

    def test_url_opener( self ):
        with uniopen.Open('https://raw.githubusercontent.com/ceumicrodata/mETL/master/tests/test_sources/test_csv_source_del_comma.csv') as rs:
            self.assertIsNotNone(rs.read())

    def test_unique_opener( self ):
        def opener_fn(url, *args, **kwargs):
            return io.open(url,'r')
        
        full_path = os.path.abspath('uniopen/__init__.py')
        with uniopen.Open('ile:///{}'.format(full_path), \
                opener = opener_fn ) as rs:
            self.assertIsNotNone(rs.read())
            
    def test_db_opener( self ):
        with uniopen.Open('sqlite:///uniopen/tests/source/sqlite.db') as rs:
            self.assertIsNotNone(rs)
            
    def __test_redshift_opener( self ):
        with uniopen.Open('redshift://username:password@endpoint:port/database') as rs:
            self.assertIsNotNone(rs)
            
    def __test_s3_opener( self ):
        with uniopen.Open('s3://key_id:secret_key@bucket/filename.txt') as rs:
            self.assertIsNotNone(rs)

    def __test_ssh_opener( self ):
        with uniopen.Open('ssh://username:password@host/file/path', 'r') as rs:
            self.assertIsNotNone(rs)
