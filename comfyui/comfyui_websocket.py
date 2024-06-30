# This is an example that uses the websockets api to know when a prompt execution is done
# Once the prompt execution is done it downloads the images using the /history endpoint

import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
from io import BytesIO
from PIL import Image
import random

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


def readfile(name, mode="r"):
    with open(name, mode) as f:
        return f.read()


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())["prompt_id"]


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(
        "http://{}/view?{}".format(server_address, url_values)
    ) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen(
        "http://{}/history/{}".format(server_address, prompt_id)
    ) as response:
        return json.loads(response.read())


def get_images(ws, prompt_id):
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history["outputs"]:
        for node_id in history["outputs"]:
            node_output = history["outputs"][node_id]
            if "images" in node_output:
                images_output = []
                for image in node_output["images"]:
                    image_data = get_image(
                        image["filename"], image["subfolder"], image["type"]
                    )
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

def process_first_image(images):
    # 获取第一个node_id下的所有image_data
    first_node_images = images.get(next(iter(images), []), [])  # 默认获取第一个key的值，如果images为空则返回空列表
    
    if first_node_images:  # 确保列表不为空
        # 处理第一个image_data
        image_data = first_node_images[0]
        
        # 将image_data转换为PIL Image对象并保存为BytesIO
        image = Image.open(BytesIO(image_data))
        byte_arr = BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        
        return byte_arr
    else:
        return None  # 或者根据需要处理没有图像的情况

def get_images_from_comfyui(prompt:str):
    print("[get_images_from_comfyui]===============start")
    workflow = json.loads(readfile("workflow/basic.json"))
    workflow["6"]["inputs"]["text"] = prompt

    workflow["3"]["inputs"]["seed"] = random.randint(1, 1000000000)

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    prompt_id = queue_prompt(workflow)
    images = get_images(ws, prompt_id)
    print("[get_images_from_comfyui]===============end")
    return process_first_image(images)
    


if __name__ == "__main__":
    prompt = json.loads(readfile("workflow/basic.json"))
    prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

    # set the seed for our KSampler node
    prompt["3"]["inputs"]["seed"] = 5

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    prompt_id = queue_prompt(prompt)
    images = get_images(ws, prompt_id)

    # Commented out code to display the output images:
    process_first_image(images)

