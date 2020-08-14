import logging
import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from jwt import InvalidSignatureError
from flask_cors import CORS, cross_origin
import pydicom
import cv2
import os
from glob import glob

load_dotenv()
logging.basicConfig(level=int(os.getenv("DEBUG_LEVEL")))

# Create the application instance
app = Flask(__name__)
CORS(app)


# Create a URL route in our application for "/"
@app.route('/', methods=['POST'])
@cross_origin()
def find_mask():
    if 'dicom' in request.files:
        if not request.files['dicom']:
            return jsonify(error="dicom missing")

    tmp_folder = os.getcwd() + "/tmp/"
    for file in glob(tmp_folder + "*"):
        os.remove(file)
    dicom = request.files['dicom']
    dicom.save(os.path.join(tmp_folder, dicom.filename))
    dataset = pydicom.dcmread(tmp_folder + dicom.filename)

    print("Filename.........:", dicom.filename)
    print("Storage type.....:", dataset.SOPClassUID)
    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patient's name...:", display_name)
    print("Patient id.......:", dataset.PatientID)
    print("Modality.........:", dataset.Modality)
    print("Study Date.......:", dataset.StudyDate)

    if 'PixelData' in dataset:
        rows = int(dataset.Rows)
        cols = int(dataset.Columns)
        print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
            rows=rows, cols=cols, size=len(dataset.PixelData)))
        if 'PixelSpacing' in dataset:
            print("Pixel spacing....:", dataset.PixelSpacing)
    print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

    if 'response' in request.form and request.form['response'] == 'png':
        cv2.imwrite(os.path.join(tmp_folder, dicom.filename.replace('.dcm', '.png')), dataset.pixel_array)
        return send_file(tmp_folder + dicom.filename.replace(".dcm", ".png"), mimetype='image/png')
    else:
        return jsonify(name=display_name,
                       id=dataset.PatientID,
                       modality=dataset.Modality,
                       study_date=dataset.StudyDate)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    # http_server = WSGIServer(('', 4254), app)
    # http_server.serve_forever()
    app.run(debug=True, port=4242, host='0.0.0.0')
