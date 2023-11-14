from .Model import Model

# Decorators syntax:
# https://realpython.com/primer-on-python-decorators/#both-please-but-never-mind-the-bread

def model_decorator(_func=None, *, contract=Model):
    
    def model_decorator_implementation(func):
        if not issubclass(contract, Model):
            raise Exception("Provided contract is not a subclass of Model")

        class _FunctionModel(contract):
            def call(self, *args, **kwargs):
                return func(*args, **kwargs)
        
        function_model = _FunctionModel()
        return function_model
    
    if _func is None:
        return model_decorator_implementation
    else:
        return model_decorator_implementation(_func)
