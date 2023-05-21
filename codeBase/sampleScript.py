import sys

print("Hello World")
try:
    print(f"Selected {sys.argv[1]}")
except IndexError:
    print("None selected")
    
