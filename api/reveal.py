from io import BytesIO
from PIL import Image

from sanic import Sanic, response

from api._stegano import detect, reveal


app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({"error": "BAD_INPUT"})
    files = request.files["files"]
    if len(files) < 1:
        return response.json({"error": "BAD_INPUT"})

    img_file = files[0]
    img_buffer = img_file.body

    img = Image.open(BytesIO(img_buffer))

    if not detect(img):
        return response.json({"error": "PAYLOAD_NOT_EXISTS"})

    try:
        payload_buffer = reveal(img)
        return response.raw(payload_buffer)
    except Exception as e:
        print(e)
        return response.json({}, status=500)
