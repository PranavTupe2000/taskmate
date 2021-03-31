import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR,".env"))

print(env('DJANGO_DEBUG'))

print("test")