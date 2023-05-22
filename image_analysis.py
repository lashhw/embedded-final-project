import http
import json
import tempfile
import os


headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '69f845d5046744b78057cc952245e1ac',
}

PEOPLE_CONFIDENCE_THRESHOLD = 0.8


def image_analysis(camera):
    filename = f"{tempfile.mktemp()}.png"
    camera.capture(filename)
    result = None

    try:
        with open(filename, 'rb') as f:
            data = f.read()
        conn = http.client.HTTPSConnection('nycu-embedded-cv.cognitiveservices.azure.com')
        conn.request(
            "POST",
            f"/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=read,caption,objects,people",
            data,
            headers
        )
        response = conn.getresponse().read()
        j = json.loads(response)
        result = {}
        result["caption"] = j["captionResult"]["text"]
        result["objects"] = [sorted(obj["tags"], key=lambda x: x["confidence"], reverse=True)[0]["name"] for obj in j["objectsResult"]["values"]]
        result["text"] = j["readResult"]["content"]
        result["people_count"] = sum(1 for x in j["peopleResult"]["values"] if x["confidence"] > PEOPLE_CONFIDENCE_THRESHOLD)
        conn.close()
    except Exception as e:
        print(f"[Error] {e}") 

    os.system(f"rm -f {filename}")

    return result