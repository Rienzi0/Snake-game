from env_0 import *
env = env()
env.Ready()
env.Start()

while True:
    env.Step([0,0,1])
    env.get_state()

    