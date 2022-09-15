import functools
import os
import pickle

ENABLE_CACHING = False


def cache_result_to_file(cache_filename):
    script_path = os.path.split(__file__)[0]
    cache_dir_path = os.path.join(script_path, "cached_objects")
    cache_file_path = os.path.join(cache_dir_path, cache_filename)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not ENABLE_CACHING:
                return func(*args, **kwargs)
            if os.path.isfile(cache_file_path):
                with open(cache_file_path, 'rb') as cache_file:
                    return pickle.load(cache_file)
            ret = func(*args, **kwargs)
            if not os.path.isdir(cache_dir_path):
                os.mkdir(cache_dir_path)
            with open(cache_file_path, 'wb') as cache_file:
                pickle.dump(ret, cache_file)
            return ret
        return wrapper
    return decorator
