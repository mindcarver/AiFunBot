import uuid
import json
import urllib.request
import websocket


class ImageGenerationService:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.websocket = None
        self.client_id =None

    def open_websocket_connection(self):
        self.client_id = str(uuid.uuid4())
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        return self.client_id

    def close_websocket_connection(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None
            
    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(p).encode('utf-8')
        req =  urllib.request.Request("http://{}/prompt".format(self.server_address), data=data, headers=headers)
        return json.loads(urllib.request.urlopen(req).read())
        
    def get_history(self,prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())    
    
    def get_images(self,prompt_id, allow_preview = False):
        output_images = []

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            output_data = {}
            if 'images' in node_output:
                for image in node_output['images']:
                    if allow_preview and image['type'] == 'temp':
                        preview_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        output_data['image_data'] = preview_data
                    if image['type'] == 'output':
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        output_data['image_data'] = image_data
            output_data['file_name'] = image['filename']
            output_data['type'] = image['type']
            output_images.append(output_data)

        return output_images

    def get_image(self,filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

def test_comfyui_websocket():
    service = ImageGenerationService()
    service.open_websocket_connection()
    workflow_api = json.loads(readfile("workflow/basic.json"))
    promot_id = service.queue_prompt(workflow_api)
    print(promot_id)
    imgs = service.get_images(promot_id)
    print(imgs)
    

def readfile(name, mode="r"):
    with open(name, mode) as f:
        return f.read()
    
if __name__ == "__main__":  
    test_comfyui_websocket()
                  