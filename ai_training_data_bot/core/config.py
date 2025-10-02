DEFAULTS = {
    "chunk_size": 512,
    "max_workers": 4,
}

def get(key, default=None):
    return DEFAULTS.get(key, default)

