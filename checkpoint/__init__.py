from functools import wraps
import gzip as gziplib
import dill
import pickle
import simplejson

def checkpoint(filename=None, format='dill', gzip=False):
  """
  A decorator that either loads the result from disk (if possible) or runs the function
  The format can be either pkl, dill, or json
  If gzip is set, the results are gzipe'ed
  """
  myopen = gziplib.open if gzip else open
  formatting = {
    'dill': dill,
    'pkl': pickle,
    'json': simplejson,
  }[format]

  def decorator(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
      if filename is None:
        filename = '--'.join([str(func)] + map(str, args) + [k + v for k, v in kwargs.iteritems()])
      try:
        with myopen(filename) as fh:
          return formatting.load(fh)
      except IOError:
        result = func(*args, **kwargs)
        with myopen(filename, "wb") as fh:
          formatting.dump(result, fh)
        return result
    return decorated_func
  return decorator
