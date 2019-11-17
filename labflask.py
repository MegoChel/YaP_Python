import os
from flask import Flask, send_file, request
from werkzeug.utils import secure_filename
app = Flask(__name__)
root_dir = os.path.abspath(os.path.dirname(__file__))
hostName = "127.0.0.1"
hostPort = 5000
UPLOAD_FOLDER = root_dir
ALLOWED_EXTENSIONS = frozenset(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class MyException(Exception):
    status_code = 400
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        
class FileManager:
	@staticmethod
	def preview_file(path):
		if not os.path.isfile(path):
			raise MyException("You cannot preview directory", status_code=400)
		if os.path.exists(path):
			return send_file(os.path.abspath(path))
		raise MyException("File not exist", status_code=400)

	@staticmethod
	def download_file(path):
		if not os.path.isfile(path):
			raise MyException("You cannot download directory", status_code=400)
		if os.path.exists(path):
			return send_file(os.path.abspath(path), as_attachment=True)
		raise MyException("File not exist", status_code=400)

	@staticmethod
	def delelte_file_or_empty_dir(path):
		if not os.path.exists(path):
			raise MyException("Not found", status_code=400)
		if os.path.isfile(path) or os.path.islink(path):
			os.remove(path)
		else:
			os.rmdir(path)
            
	@staticmethod
	def create_dir(path):
		if os.path.exists(path):
			raise MyException("Folder already exists", status_code=400)
		os.makedirs(path)


# Реализация для корневой папки
@app.route('/')
def get_root_list():
	files = os.listdir(root_dir)
	html_code = '<h2><a href="http://' + hostName + ':' + str(hostPort) + '/upload"> Upload to / </a></h2>'
	for el in files:
		if os.path.isfile(root_dir + '/' + el):
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/previewFile/' + el + '">' + el + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/downloadFile/' + el + '">' + ' [dwnld]' + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + el + '">' + ' [rmv]' + '</a>'
			html_code += '</li>'
		else:
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/' + el + '">' + el + '/' + '</a>'
			if os.listdir(root_dir + '/' + el) == []:
				html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + el + '">' + ' [rmv]' + '</a>'
			html_code += '</li>'
	return ('<meta charset="UTF-8"/>' + html_code)

#Реализация для остальных папок
@app.route('/<path:subpath>')
def get_list(subpath):
	directory = root_dir + '/' + subpath
	files = os.listdir(directory)
	html_code = '<h2><a href="http://' + hostName + ':' + str(hostPort) + '/upload/' + subpath + '"> Upload to /' + subpath + '</a></h2>'
	for el in files:
		if os.path.isfile(root_dir + '/' + subpath + '/' + el):
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/previewFile/' + subpath + '/' + el + '">' + el + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/downloadFile/' + subpath + '/' + el + '">' + ' [dwnld]' + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + subpath + '/' + el + '">' + ' [rmv]' + '</a>'
			html_code += '</li>'
		else:
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/' + subpath + '/' + el + '">' + el + '/' + '</a>'
			if os.listdir(directory + '/' + el) == []:
				html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + subpath + '/' + el + '">' + ' [rmv]' + '</a>'
			html_code += '</li>'
	return ('<meta charset="UTF-8"/>' + html_code)



@app.route("/previewFile/<path:subpath>")
def preview_file(subpath):
	File_dir = root_dir + '/' + subpath
	return FileManager.preview_file(File_dir)

@app.route("/downloadFile/<path:subpath>")
def download_file(subpath):
	File_dir = root_dir + '/' + subpath
	return FileManager.download_file(File_dir)

@app.route("/delete/<path:subpath>")	
def delete(subpath):
	File_dir = root_dir + '/' + subpath
	FileManager.delelte_file_or_empty_dir(File_dir)
	return "Success"

@app.route("/createDir/<path:subpath>")
def __create_dir(subpath):
	directory = root_dir + '/' + subpath
	FileManager.create_dir(directory)
	return "Success"

@app.route('/upload/<path:subpath>')
def upload_file(subpath):
	File_dir = root_dir + '/' + subpath
	app.config['UPLOAD_FOLDER'] = File_dir
	return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

# Реализация для скачивания из корневой папки
@app.route('/upload')
def upload_file_in_root():
	directory = root_dir
	app.config['UPLOAD_FOLDER'] = directory
	return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_2():
	def allowed_file(filename):
		return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	if request.method == 'POST':
		f = request.files['file']
		if allowed_file(f.filename):
			f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
			return 'file uploaded successfully'
		return "Bad file name"

if __name__ == '__main__':
    app.run(debug=True)