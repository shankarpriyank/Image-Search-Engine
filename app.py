# create flask app
from flask import Flask, request, jsonify, render_template
from src.search import search
from src.caption import predict
# CORS flask
from flask_cors import CORS
import os
from PIL import Image
from src.ib64 import image_to_base64
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*",
            "allow_headers": "*", "expose_headers": "*"}})


@app.route('/', methods=['POST'])
def create_task():
    if request.method == 'POST':
        recievedFile = request.files['file']
        if recievedFile.filename != '':
            recievedFile.save(str(recievedFile.filename))
            image_path = str(recievedFile.filename)
            search_query = predict(image_path)
            print(search_query)  # this is the caption
            os.remove(image_path)  # remove the image from the server
            lt = search(search_query)  # this is the list of images
            # convert the images to base64
            lt = [image_to_base64(Image.open(
                f"getter/{photo_id}.jpg")) for photo_id in lt]
            for i in range(len(lt)):
                lt[i] = str(lt[i])
            for i in range(len(lt)):
                x = ''
                for j in range(len(lt[i])-5):
                    if j < 2:
                        continue
                    x += str(lt[i][j])
                lt[i] = x
            return lt
            # str(lt) # return the list of images
        else:
            return "No file recieved"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
