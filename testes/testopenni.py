import sys, pygame
from openni import openni2, nite2, utils

#openni2.initialize("/home/thiago/OpenNI-Linux-x64-2.2/Redist")
#nite2.initialize("/home/thiago/NiTE-2.0.0/Redist")
#openni2.initialize("/home/leonardo/Downloads/OpenNI-Linux-x64-2.2/Redist")
openni2.initialize("/home/leonardo/Tcc/OpenNI-Linux-x64-2.2/Redist")
#nite2.initialize("/home/leonardo/Downloads/NiTE-Linux-x64-2.2/Redist")
nite2.initialize("/home/leonardo/Tcc/NiTE-2.0.0/Redist")

dev = openni2.Device.open_any()
device_info = dev.get_device_info()

print(device_info)

try:
    userTracker = nite2.UserTracker(dev)
except utils.NiteError as ne:
    print("Unable to start the NiTE human tracker. Check the error messages in the console. Model data (s.dat, h.dat...) might be inaccessible.")
    print(ne)
    sys.exit(-1)


while True:
    
    frame = userTracker.read_frame()
    depth_frame = frame.get_depth_frame()

    if frame.users:
        for user in frame.users:
            print("Skeleton state: ", user.skeleton.state)
            if user.is_new():
                print("New human detected! ID: %d Calibrating...", user.id)
                userTracker.start_skeleton_tracking(user.id)
            elif user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED:            
                print("New data tracked")                
                head = user.skeleton.joints[nite2.JointType.NITE_JOINT_HEAD]

                confidence = head.positionConfidence
                print user.id
                print("Head: (x:%dmm, y:%dmm, z:%dmm), confidence: %.2f" % (
                                                                    head.position.x,
                                                                    head.position.y,
                                                                    head.position.z,
                                                                    confidence))
    else:
        print("No users")

nite2.unload()
openni2.unload()
