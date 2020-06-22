from functools import wraps

def add_method(cls):
	def decorator(func):
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			return func(*args, **kwargs)
		setattr(cls, func.__name__, wrapper)
		return func
	return decorator

def add_method(cls):
	def decorator(func):
		setattr(cls, func.__name__, func)
		return func
	return decorator