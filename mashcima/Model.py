from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from mashcima.Space import Space
from typing import Optional
from abc import ABC, abstractmethod


class PreviewServer(BaseHTTPRequestHandler):
    def do_GET(self):
        html = "Hello world! " + self.path
        html_bytes = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(html_bytes))
        self.end_headers()
        self.wfile.write(html_bytes)
    
    def do_POST(self):
        self.do_GET()


class Model(ABC):
    """Base class for all generative models"""
    def __init__(self):
        self.space: Optional[Space] = None

    def print(self):
        s = HTTPServer(("0.0.0.0", 8080), PreviewServer)
        webbrowser.open_new("http://localhost:8080")
        s.serve_forever()
    
    def validate_input(self, *args, **kwargs):
        pass
    
    def validate_output(self, *args, **kwargs):
        pass

    @abstractmethod
    def call(self, *args, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        # space context
        if Space.current is None:
            raise Exception("Model has to be executed in the context of a space")
        self.space = Space.current

        # extract arguments from space
        # ... modify args and kwargs

        self.validate_input(*args, **kwargs)

        # execute the model
        returned = self.call(*args, **kwargs)

        if isinstance(returned, dict):
            self.validate_output(**returned)
        
        # populate space
        if isinstance(returned, dict):
            for key in returned.keys():
                self.space[key] = returned[key]
        
        return returned
