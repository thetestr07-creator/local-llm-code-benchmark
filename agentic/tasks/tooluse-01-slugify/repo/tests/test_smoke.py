import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from textkit.normalize import slugify

assert slugify("Hello World") == "hello-world"
print("smoke OK")
