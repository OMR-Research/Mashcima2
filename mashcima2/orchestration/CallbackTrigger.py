from .Callback import Callback
from typing import List


class CallbackTrigger:
    """Class responsible for registering and triggering model callbacks"""
    def __init__(self):
        self.callbacks: List[Callback] = []
    
    def add_callback(self, callback: Callback):
        self.callbacks.append(callback)
    
    def trigger_on_sample_begin(self):
        for c in self.callbacks:
            c.on_sample_begin()
    
    def trigger_on_sample_end(self):
        for c in self.callbacks:
            c.on_sample_end()
