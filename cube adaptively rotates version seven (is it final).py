from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import degrees, atan2
import numpy as np
app = Ursina()

def angle_between_vectors(u, v):
    dot_product = sum(i*j for i, j in zip(u, v))
    norm_u = math.sqrt(sum(i**2 for i in u))
    norm_v = math.sqrt(sum(i**2 for i in v))
    cos_theta = dot_product / (norm_u * norm_v)
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)
    return angle_rad, angle_deg

application.frame_rate = 0

terr = Terrain('heightmap', skip=25)
terrain = Entity(model=terr, scale=40, texture='grass', collider='mesh', debug=True)



terrain.y -= 10

# Creating a player
player = FirstPersonController()
player.y = 20

rotationtoGive = 180

cubeObject2 = Entity(model="hatchback.obj", visible=True, rotation_y=rotationtoGive, scale=(1,1,1), texture="hatchback-orange.png")
#cubeObject2 = Entity(model="cube", visible=True, rotation_y=rotationtoGive, scale=(3,1,1))
cubeControllingComponent2 = Entity()


notGrounded = True

cubeControllingComponent2.y = 6
cubeControllingComponent2.x = 17
cubeControllingComponent2.z= 3

prevWorldNormal = Vec3(0,0,0)

def update():
    global prevWorldNormal, current_y_rotation,notGrounded, rotationtoGive

    if held_keys["g"]:
        cubeControllingComponent2.y += 5 * time.dt
        #cubeControllingComponent2.rotation = Vec3(0, 0, 0)
    if held_keys["h"]:
        rotationtoGive += 50*time.dt
    if held_keys["j"]:
        rotationtoGive -= 50*time.dt

    origin = cubeControllingComponent2.position
    hit_info = raycast(origin, (0,-1,0), ignore=(cubeObject2,), distance=2, debug=True)

    #cubeControllingComponent2.z -= 0.5*time.dt

    cubeObject2.rotation_x = lerp(cubeObject2.rotation_x, cubeControllingComponent2.rotation_x, 20 * time.dt)
    cubeObject2.rotation_z = lerp(cubeObject2.rotation_z, cubeControllingComponent2.rotation_z, 20 * time.dt)
    cubeObject2.rotation_y = rotationtoGive
    cubeControllingComponent2.rotation_y = rotationtoGive
    cubeObject2.position = cubeControllingComponent2.position

    # Adjust rotation based on terrain if grounded
    if hit_info.hit:
        normal = hit_info.world_normal
        # debug = Entity(model="sphere", color=color.yellow, position=cubeControllingComponent2.position + cubeObject2.back, scale=0.1)
        cubeControllingComponent2.look_at(cubeControllingComponent2.position + normal, axis="up", up=cubeControllingComponent2.back)
        #print(cubeControllingComponent2.rotation)
        #cubeControllingComponent2.rotation_y = 0 + rotationtoGive
        # debug2 = Entity(model="sphere", color=color.red, position=cubeControllingComponent2.position + cubeObject2.back, scale=0.1)
        #cubeObject2.look_at_2d(cubeControllingComponent2.position + Vec3(-1*normal.x,0,1), axis="y")

    else:
        cubeControllingComponent2.y -= 2 * time.dt
        cubeControllingComponent2.rotation = lerp(cubeControllingComponent2.rotation, Vec3(0,0,0), 5 * time.dt)




app.run()