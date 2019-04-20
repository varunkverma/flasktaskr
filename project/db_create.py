# project/db_create.py

import sqlite3;
from _config import DATABASE_PATH;

with sqlite3.connect(DATABASE_PATH) as connection:
	cursor=connection.cursor();

	cursor.execute("""
		CREATE TABLE Tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL, due_date TEXT NOT NULL,
		 priority INTEGER NOT NULL, status INTEGER NOT NULL)
		""");
	#some summy data

	cursor.execute('INSERT INTO Tasks (name, due_date,priority, status)'
					'VALUES("Finishing this tutorial","04/20/2019",10,1)' );

	cursor.execute('INSERT INTO Tasks (name, due_date,priority, status)'
					'VALUES("Finishing this course","06/20/2019",10,1)' );

	