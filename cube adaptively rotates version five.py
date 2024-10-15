from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import degrees, atan2, sin, cos
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
cube = Entity(model=terr, scale=40, texture='grass', collider='mesh', debug=True)



cube.y -= 10

# Creating a player
player = FirstPersonController()
player.y = 20

rotationtoGive = 45

cubeObject2 = Entity(model="hatchback.obj", visible=True, rotation_y=rotationtoGive, scale=(1,1,1), texture="hatchback-orange.png")
#cubeObject2 = Entity(model="cube", visible=True, rotation_y=rotationtoGive, scale=(3,1,1))
cubeControllingComponent2 = Entity()
cubeObject2.parent = cubeControllingComponent2

notGrounded = True

cubeControllingComponent2.y = 12
cubeControllingComponent2.x = 2
cubeControllingComponent2.z= 16

prevWorldNormal = Vec3(0,0,0)
current_y_rotation = 0  # Track the y-rotation separately

def update():
    global prevWorldNormal, current_y_rotation,notGrounded

    if held_keys["g"]:
        cubeControllingComponent2.y += 5 * time.dt
        cubeControllingComponent2.rotation = Vec3(0, 0, 0)
        cubeObject2.rotation_y = rotationtoGive

    origin = cubeControllingComponent2.position
    hit_info = raycast(origin, (0,-1,0), ignore=(cubeObject2,), distance=2, debug=True)

    # Adjust rotation based on terrain if grounded
    if hit_info.hit:
        if prevWorldNormal != hit_info.world_normal or notGrounded:
            prevWorldNormal = hit_info.world_normal
            notGrounded = False

            normal = hit_info.world_normal
            cubeControllingComponent2.look_at_2d(cubeControllingComponent2.position + normal, axis="z")
            debug = Entity(model="sphere", color=color.yellow, position=cubeControllingComponent2.position + cubeObject2.right, scale=0.1)
            xv1 = cubeControllingComponent2.right[0]
            yv1 = cubeControllingComponent2.right[1]
            zv1 = cubeControllingComponent2.right[2]
            cubeControllingComponent2.rotation = Vec3(0,0,0)
            cubeControllingComponent2.look_at(cubeControllingComponent2.position + normal,axis="up")
            debug2 = Entity(model="sphere", color=color.red,position=cubeControllingComponent2.position + cubeObject2.left, scale=0.1)
            xv2 = cubeControllingComponent2.left[0]
            yv2 = cubeControllingComponent2.left[1]
            zv2 = cubeControllingComponent2.left[2]
            angle = angle_between_vectors([xv1,yv1,zv1],[xv2,yv2,zv2] )
            if yv1 > 0:
                cubeObject2.rotation_y -= angle[1]
            else:
                cubeObject2.rotation_y += angle[1]
            debug3 = Entity(model="sphere", color=color.blue,position=cubeControllingComponent2.position + cubeObject2.left, scale=0.1)
            cubeObject2.rotation_y += 180
            print(debug3.x - debug.x, debug3.z - debug.z)
            #print(-degrees(atan2(debug3.x - debug.x,debug3.z - debug.z)))
            print(cubeObject2.rotation_y)

    else:
        cubeControllingComponent2.y -= 2 * time.dt
        cubeControllingComponent2.rotation = Vec3(0, 0, 0)
        cubeObject2.rotation_y = rotationtoGive
        notGrounded = True



app.run()