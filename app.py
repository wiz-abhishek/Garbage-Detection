from flask import Flask,render_template,request,redirect,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(200), nullable = False, unique = True)

with app.app_context():
    db.create_all() 

@app.route('/')
def index():
    
    files = File.query.all()
    return render_template('index.html', files = files)    


@app.route('/uploads', methods=['POST'])   
def uploads():
    if request.method == 'POST':
        files = request.files.getlist('files')

        for file in files:

            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_file = File(filename = filename)
            db.session.add(new_file)
            try:
               db.session.commit()
            except:
                print("The file has already been uploaded!")
                return '<h1>The file has already been uploaded!</h1>'

        return redirect('/')
    return 'something wrong please try again!'  


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:file_id>')
def delete(file_id):

    file = File.query.get_or_404(file_id)
    filename = file.filename

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)

    db.session.delete(file)
    db.session.commit()

    return redirect('/')

# @app.route('/predict<int:file_id>')
# def plot(file_id):
#    file = File.query.get_or_404(file_id)
#    filename = file.filename
#    img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
#    data = read_img(img_file_path)
#    return render_template("result.html", prediction = prediction)   


if __name__ == '__main__':
    app.run(debug=True)   