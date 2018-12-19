from aiohttp import web
import tempfile
import uuid
import os
import json
from pytranslive import Transcoder, TranscodeJob, TranscodeOptions

transcoder = Transcoder("", "/dev/dri/renderD129")

routes = web.RouteTableDef()

transcode_dir = tempfile.mkdtemp()

transcode_jobs = {}

@routes.post("/jobs")
async def transcode(request):
    if "url" in request.query:
        url = request.query["url"]

        transcode_id = str(uuid.uuid4())

        output_dir = transcode_dir + os.sep + transcode_id
        os.mkdir(output_dir)

        transcode_job = transcoder.transcode(url, output_dir, "stream.m3u8")
        transcode_job.start()

        transcode_jobs[transcode_id] = transcode_job

        resp = {
            "id": transcode_id,
            "url_path": "/output/" + transcode_id + "/stream.m3u8"
        }

        return web.Response(text=json.dumps(resp), content_type="application/json")

    return web.Response(status=400, text="URL missing")

@routes.delete("/jobs/{id}")
async def delete(request):

    transcode_id = request.match_info.get("id")
    if transcode_id and transcode_id in transcode_jobs:
        transcode_jobs[transcode_id].delete()
        return web.Response()

    return web.Response(status=400, text="No job with ID " + transcode_id)

@routes.get("/jobs/{id}/stop")
async def stop(request):

    transcode_id = request.match_info.get("id")
    if transcode_id and transcode_id in transcode_jobs:
        transcode_jobs[transcode_id].stop()
        return web.Response()

    return web.Response(status=400, text="Job ID missing or wrong")

app = web.Application()
routes.static("/output", transcode_dir)
app.add_routes(routes)
web.run_app(app, port=9999)
