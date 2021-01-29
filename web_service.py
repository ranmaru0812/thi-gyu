import face_recognition
from flask import Flask, jsonify, request, redirect, render_template
import json
import subprocess
import os


# 以下の4つのファイル形式のみ許可する
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>チー牛判定機</title>
    <h1>あなたのチー牛率は！？</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # 以下はチー牛（元の画像）をの128次元特徴量にエンコードしたもの
    known_face_encoding = [-0.11040579,  0.05424782,  0.15179718,  0.02071334, -0.0657726,  -0.10343515,
                        -0.07530531, -0.1358026,   0.10000467, -0.11897585,  0.16678749, -0.07516095,
                        -0.17811184,  0.02301318, -0.08678365,  0.17069878, -0.06723175, -0.10969639,
                        -0.06430213, -0.06350441,  0.07101165,  0.05759009, -0.02604039,  0.03278423,
                        -0.03761718, -0.27082217, -0.11582725, -0.06136753,  0.06565917, -0.07112892,
                        -0.06288964,  0.04459563, -0.10689934, 0.04179727, -0.00085483,  0.09218968,
                        -0.00794301, -0.1162945,   0.22870995, -0.03446282, -0.21498536, -0.00301889,
                         0.0476355,   0.23444891,  0.17686075,  0.01330441,  0.04754907, -0.10771186,
                         0.081066,   -0.16314307,  0.02163126,  0.15220425,  0.08951616,  0.06136734,
                         0.01918219, -0.1836087,   0.00550257,  0.05794163, -0.11416318,  0.07715067,
                         0.12056482, -0.10299724, -0.06507127, -0.09004745,  0.20164195,  0.07833141,
                        -0.14463314, -0.13141687,  0.10687217, -0.23229401, -0.04254848, 0.06385166,
                        -0.16217038, -0.15036343, -0.28340042, -0.00201236, 0.42292863,  0.13498023,
                        -0.16508843,  0.0547797,  -0.02257079,  0.00552969,  0.12099879,  0.1603238,
                        -0.07571621,  0.03562711, -0.08577023,  0.02849763,  0.21207272, -0.02927457,
                        -0.01466956,  0.17746548, -0.01067175,  0.06131135, -0.06866688,  0.01800534,
                        -0.0277501,  -0.03022642, -0.02887546,  0.00900932,  0.0524117,  -0.05372276,
                         0.02926694,  0.12404613, -0.16034123,  0.12814705, -0.0254039,  0.06506681,
                         0.0435774,   0.04975387, -0.11924725, -0.03838437,  0.18468279, -0.15981971,
                         0.11475484,  0.17644173,  0.02558588,  0.07886083,  0.1110673,   0.16521899,
                        -0.01623669, -0.00163811, -0.20324866, -0.00926553,  0.03859815, -0.02626697,
                         0.08108661,  0.05410679]

    # アップロードされた画像を読み込む
    uploaded_img = face_recognition.load_image_file(file_stream)
    # アップロードされた画像のエンコード
    unknown_face_encodings = face_recognition.face_encodings(uploaded_img)

    face_found = False
    is_chigyu = False

    # 顔が検出できた場合
    if len(unknown_face_encodings) > 0:
        face_found = True
        # アップロードされた画像とチー牛がどれくらい（顔画像間距離的に）近いものなのかを判断 -> True or False
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        # チー牛である場合
        if match_results:
            is_chigyu = True

    # 顔画像間距離を出すぞ
    face_distance = os.popen("face_recognition --show-distance true ./img/ ./upload/")
    face_distance = float((face_distance.read()).strip()[-19:])
    print(face_distance)


    # チー牛の場合
    if is_chigyu:
        return render_template("out.html")
    # チー牛でない場合
    elif face_found:
        return render_template("out.html")
    # 顔すらも検出できない場合
    else:
        return render_template("onemore.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
