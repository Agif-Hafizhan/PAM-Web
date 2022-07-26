from winsound import MB_ICONASTERISK
import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

ds = pd.read_csv('DataLengkap2.csv', usecols= ['Jurusan','Matematika','Bahasa Inggris','Bahasa Indonesia','Prestasi '])

x = ds.iloc[:,:-1].values 
y = ds.iloc[:,-1].values 

encoder = LabelEncoder()

x[:,0] = encoder.fit_transform(x[:,0]) 
x[:,1] = encoder.fit_transform(x[:,1]) 
x[:,2] = encoder.fit_transform(x[:,2])
x[:,3] = encoder.fit_transform(x[:,3])
y = encoder.fit_transform(y) 

model = MultinomialNB()

model.fit(x, y)

@app.route('/')
def index():
    return render_template('index.html',Hasil = "??", Jurusan = "??", MTK = "??", BING = "??", BINDO ="??")



@app.route('/prediction', methods=['POST'])
def prediction():
    
    Jurusan = int(request.form['Jurusan'])
    MTK = int(request.form['MTK'])
    BINDO = int(request.form['BINDO'])
    BING = int(request.form['BING'])
    
    predicted = model.predict([[Jurusan, MTK, BINDO, BING]])
    
    if Jurusan == 1:
        Jurusan = "IPA"
    else :
        Jurusan = "IPS"
    
    if MTK + BING + BINDO >= 200:
        predicted = "Berprestasi"
    else:
        predicted = "Tidak Berprestasi"


    return render_template('index.html', Hasil = predicted, Jurusan = Jurusan, MTK = MTK, BINDO = BINDO, BING = BING)


if __name__ == '__main__':
    app.run(debug=True)