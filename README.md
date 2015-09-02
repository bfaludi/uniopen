# uniopen (Universal Opener)

It's so simple. You can open things with it, that's the story. Nothing more. It works with Python **2** and **3** as well.

#### Let's see the magic

Open a local file:

```python
with uniopen.Open('file.csv', 'r', encoding = 'utf-8') as rs:
	print(rs.read())
```

Open an URL:

```python
with uniopen.Open('http://goo.gl/7XZsrO') as rs:
	print(rs.read())
```

Open a Database connection:

```python
with uniopen.Open('postresql://username:password@host:port/dbname') as rs:
	print(rs.execute('SELECT * FROM table_name;'))
```

... even in Amazon Redshift:

```python
with uniopen.Open('redshift://username:password@endpoint:port/database') as rs:
	print(rs.execute('SELECT * FROM table_name;'))
```

Open a file via SSH connection:

```python
with uniopen.Open('ssh://username:password@host:port/home/username/example/file.csv', 'r') as rs:
	print(rs.read())
```

Open a file in Amazon S3 bucket:

```python
with uniopen.Open('s3://key_id:secret_key@bucket/file.csv') as rs:
	print(rs.read())
```

Open a file in HFDS:

```python
with uniopen.Open('hdfs://user/hadoop/file.csv') as rs:
	print(rs.read())          
```

Enjoy!