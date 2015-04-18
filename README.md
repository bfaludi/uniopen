# Uniopen (Universal File Opener)

It's so simple. You can open files with it, that's the story. Nothing more. It works with Python **2** and **3** as well.

#### Examples

Open a local file:
	
	with uniopen.Open('file.csv', 'r') as rs:
		print(rs.read())
		
Open an URL:

	with uniopen.Open('http://goo.gl/7XZsrO') as rs:
		print(rs.read())
		
Open a Database connection:

	with uniopen.Open('postresql://username:password@host:port/dbname') as rs:
		print(rs.execute('SELECT * FROM table_name;'))
		
Enjoy!