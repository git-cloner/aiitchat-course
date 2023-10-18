import asyncio
import json
import time
import datetime
import os
import aiohttp_cors
import requests
from aiohttp import web


def getAnswerFromChatGLM6b_v2(contextx):
    data = json.dumps(contextx)
    url = "http://127.0.0.1:8001/stream"
    headers = {'content-type': 'application/json;charset=utf-8'}
    r = requests.post(url, data=data, headers=headers)
    res = r.json()
    if r.status_code == 200:
        return res
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'response': '算力不足，请稍候再试！[stop]', 'history': [], 'status': 200, 'time': now}


async def stream_v2(request):
    token = request.query.get('token')
    params = await request.json()
    context = params["context"]
    modelname = params["modelname"]
    prompt = context["prompt"]

    start = time.perf_counter()
    print(time.strftime("%Y-%m-%d %H:%M:%S",
                        time.localtime()), "request : " + prompt)
    stop = False
    if token == "123":
        result = getAnswerFromChatGLM6b_v2(context)
        stop = result["response"] .endswith("[stop]")
        if result["response"] == "":
            result["response"] = "思考中"
        if stop:
            result["response"] = result["response"].replace("[stop]", "")
    else:
        result = {'response': '[stop]', 'history': [], 'status': 200}
        result["response"] = "无效token"
        stop = True
    end = time.perf_counter()
    result["time"] = end-start
    result["stop"] = stop
    print(time.strftime("%Y-%m-%d %H:%M:%S",
                        time.localtime()), "result  : " + result["response"])
    return web.Response(
        content_type="application/json",
        text=json.dumps(result),
    )

app = web.Application()
cors = aiohttp_cors.setup(app)
app.router.add_post("/api/stream/v2", stream_v2)

for route in list(app.router.routes()):
    cors.add(route, {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

if __name__ == "__main__":
    print("Start web server")
    web.run_app(
        app, access_log=None, host="0.0.0.0", port=5001, ssl_context=None
    )
