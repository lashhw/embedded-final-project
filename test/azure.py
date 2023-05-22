import http
import urllib
import json
from operator import itemgetter

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '69f845d5046744b78057cc952245e1ac',
}

try:
    with open('image.jpeg', 'rb') as f:
        data = f.read()
    conn = http.client.HTTPSConnection('nycu-embedded-cv.cognitiveservices.azure.com')
    conn.request("POST", f"/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=read,caption,objects,people", data, headers)
    response = conn.getresponse()
    data = response.read()
    j = json.loads(data)
    print(j['captionResult']['text'])
    for obj in j['objectsResult']['values']:
        print(sorted(obj['tags'], key=itemgetter('confidence'), reverse=True)[0]['name'])
    print(j['readResult']['content'])
    people_count = sum(1 for x in j['peopleResult']['values'] if x['confidence'] > 0.8)
    print(f'number of people: {people_count}')
    conn.close()
except Exception as e:
    print(f"[Error] {e}") 
