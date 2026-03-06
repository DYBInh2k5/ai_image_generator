import os
import sys

print("Checking PyTorch DLLs...")
try:
    import torch
    print("PyTorch loaded successfully!")
except ImportError as e:
    print(f"Failed to import PyTorch: {e}")
    print("Trying to gather more specific DLL missing info...")
    try:
        # Manually load the _C DLL to see the real Windows error
        import ctypes
        import site
        
        # Build the path to the torch _C.pyd file
        packages_dir = site.getusersitepackages()
        if not os.path.exists(packages_dir):
            packages_dir = [p for p in sys.path if "site-packages" in p][0]
            
        c_dll_path = os.path.join(packages_dir, "torch", "_C.cp311-win_amd64.pyd")
        print(f"Loading {c_dll_path}...")
        
        # This will trigger the ugly but precise Windows ctypes error
        ctypes.WinDLL(c_dll_path)
    except Exception as ex:
        print(f"Exact DLL Error: {ex}")
