from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import degrees, atan2
import numpy as np
from ursina.scripts.noclip_mode import NoclipMode

app = Ursina()

application.frame_rate = 0

terr = Terrain('heightmap', skip=25)
terrain = Entity(model=terr, scale=40, texture='grass', collider='mesh', debug=True)



terrain.y -= 10

# Creating a player
player = FirstPersonController(NoclipMode=True)
player.y = 20

rotationtoGive = 90

cubeControllingComponent2 = Entity(model="hatchback.obj", visible=True, rotation_y=rotationtoGive, scale=(1,1,1), texture="hatchback-orange.png")
test = Entity(model="hatchback.obj", visible=False, rotation_y=rotationtoGive, scale=(1,1,1), texture="hatchback-orange.png")


notGrounded = True

cubeControllingComponent2.y = 9
cubeControllingComponent2.x = 14
cubeControllingComponent2.z= 3

prevWorldNormal = Vec3(0,0,0)

def update():
    global prevWorldNormal, current_y_rotation,notGrounded, rotationtoGive

    if held_keys["g"]:
        cubeControllingComponent2.y += 5 * time.dt
    if held_keys["h"]:
        rotationtoGive += 50*time.dt
    if held_keys["b"]:
        cubeControllingComponent2.x -= 1*time.dt
    if held_keys["n"]:
        cubeControllingComponent2.x += 1*time.dt

    origin = cubeControllingComponent2.position
    hit_info = raycast(origin, (0,-1,0), ignore=(cubeControllingComponent2,), distance=2, debug=True)

    #cubeControllingComponent2.z -= 0.5*time.dt
    cubeControllingComponent2.rotation_y = rotationtoGive

    # Adjust rotation based on terrain if grounded
    test.position = cubeControllingComponent2.position
    if hit_info.hit:

        normal = hit_info.world_normal
        cubeControllingComponent2.look_at(cubeControllingComponent2.position + normal, axis="up", up=cubeControllingComponent2.back)

    else:
        cubeControllingComponent2.y -= 2 * time.dt
        cubeControllingComponent2.rotation = lerp(cubeControllingComponent2.rotation, Vec3(0,0,0), 0.1* time.dt)

app.run()