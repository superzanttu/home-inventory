sqlite3 hiapp.db .schema > ./backup/hiapp_schema.sql
sqlite3 hiapp.db .dump > ./backup/hiapp_data.sql

sqlite3 todo.db .schema > ./backup/todo_schema.sql
sqlite3 todo.db .dump > ./backup/todo_data.sql

ls -la  ./backup/

