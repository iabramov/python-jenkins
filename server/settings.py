import os.path, logging, sqlite3
import pathlib

project_path = os.path.dirname(os.path.abspath(__file__))
sqlite_file_path = project_path+'/users.sqlite'
log_file_path = project_path+'/logs/python-test.log'

# HTTP host
http_host = ''
# HTTP port
http_port = 8080

pathlib.Path(project_path+'/logs').mkdir(parents=True, exist_ok=True)