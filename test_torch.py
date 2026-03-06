import traceback
try:
    import torch
    print('SUCCESS')
except Exception:
    traceback.print_exc()
