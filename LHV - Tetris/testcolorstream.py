#!/usr/bin/python
#-*-coding: utf-8

import sys, pygame
import numpy as np
from openni import openni2, nite2, utils
from openni import _openni2 as c_api

BLACK = (0, 0, 0)

# Função para desenhar as juntas na surface chamada screen.
# Por enquanto pega só cabeça e mãos e desenha um pequeno círculo azul (?) de 10 pixels de diâmetro
def draw_joints(screen, joints):
    head = joints[nite2.JointType.NITE_JOINT_HEAD]
    leftHand = joints[nite2.JointType.NITE_JOINT_LEFT_HAND]
    rightHand = joints[nite2.JointType.NITE_JOINT_RIGHT_HAND]

    list = (head, leftHand, rightHand)

    for joint in list:
        (depthX, depthY) = userTracker.convert_joint_coordinates_to_depth(joint.position.x, joint.position.y,
                                                                          joint.position.z)
        pygame.draw.circle(screen, (0, 0, 255), (int(depthX), int(depthY)), 10)

# Utiliza truques do pygame.font para desenhar o texto diretamente na tela - Não funcional ainda...
def screen_print(screen, msg):
    f = pygame.font.SysFont("arial", 9)
    surface = f.render(msg, True, BLACK)

    screen.blit(surface, (10, 10))

pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([640, 480], 0, 24);

# Substituir pelo path de instalação do OpenNI e do NiTE (versão ****2.0***** apenas)
#openni2.initialize("/home/thiago/OpenNI-Linux-x64-2.2/Redist")
#nite2.initialize("/home/thiago/NiTE-2.0.0/Redist")

#openni2.initialize("/home/leonardo/Downloads/OpenNI-Linux-x64-2.2/Redist")
openni2.initialize("/home/leonardo/Tcc/OpenNI-Linux-x64-2.2/Redist")
#nite2.initialize("/home/leonardo/Downloads/NiTE-Linux-x64-2.2/Redist")
nite2.initialize("/home/leonardo/Tcc/NiTE-2.0.0/Redist")

# Abre o primeiro dispositivo disponível (e normalmente o único)
dev = openni2.Device.open_any()

# sensor_info pega a informação do sensor escolhido (em geral usamos o DEPTH e o COLOR)
sensor_info = dev.get_sensor_info(openni2.SENSOR_COLOR)

print sensor_info.videoModes

# Kinect 1 funciona a 640x480
color_stream = dev.create_color_stream()
color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))
color_stream.start()

# Tentativa de inverter as cores - ainda não está 100%...
r, g, b, a = screen.get_masks();
screen.set_masks((b, g, r, a));

try:
    userTracker = nite2.UserTracker(dev)
except utils.NiteError as ne:
    print("Unable to start the NiTE human tracker. Check the error messages in the console. Model data (s.dat, h.dat...) might be inaccessible.")
    print(ne)
    sys.exit(-1)

# Loop para obter cada imagem e renderizar
while True:
    frame = color_stream.read_frame()
    frame_data = frame.get_buffer_as_uint8()

    userframe = userTracker.read_frame();
    depthframe = userframe.get_depth_frame();

    # Draw frame
    img = np.frombuffer(frame_data, np.uint8);

    bv = screen.get_buffer()
    bv.write(img.tostring(), 0)

    # Identificar os esqueletos na imagem
    if userframe.users:
        for user in userframe.users:
            print(screen, "Skeleton state: " + str(user.skeleton.state))
            if user.is_new():
                print("New human detected! ID: %d Calibrating...", user.id)
                userTracker.start_skeleton_tracking(user.id)
            elif user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED:
                draw_joints(screen, user.skeleton.joints)
                print("New data tracked")
                # head = user.skeleton.joints[nite2.JointType.NITE_JOINT_HEAD]
                # confidence = head.positionConfidence
                #
                # (depthX, depthY) = userTracker.convert_joint_coordinates_to_depth(head.position.x, head.position.y, head.position.z)
                #
                # print("Head: (x:%dmm, y:%dmm, z:%dmm), confidence: %.2f" % (
                #                                                     head.position.x,
                #                                                     head.position.y,
                #                                                     head.position.z,
                #                                                     confidence))
                # print("Head: (x: %d pixels, y: %d pixels" % (depthX, depthY))
                # pygame.draw.circle(screen, (0, 0, 255), (int(depthX), int(depthY)), 10)
    else:
        print("No users")

    # Terminando de desenhar tudo chamamos flip() para renderizar totalmente o buffer da tela
    pygame.display.flip();


color_stream.stop()
openni2.unload()

