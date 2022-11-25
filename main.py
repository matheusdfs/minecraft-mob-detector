import cv2
import numpy
from PIL import ImageGrab
from matplotlib import pyplot as plt

while(True):
    printscreen_pil = ImageGrab.grab()
    printscreen_numpy = numpy.array(printscreen_pil.getdata(), dtype=uint8).reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
    cv2.imshow('window', printscreen_numpy)

MIN_MATCH_COUNT = 10

img1 = cv2.imread('default_mob_skins/minecraft_zombie_head.png',0) # queryImage
img2 = cv2.imread('mario_train.jpeg',0) # trainImage

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

kps_img = cv2.drawKeypoints(
    image     = img2,
    keypoints = kp2,
    outImage  = img2
)

# matching algorythm
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2) #(tuple with matches)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = numpy.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = numpy.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = numpy.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M) # 4 coordinates

    img2 = cv2.polylines(img2,[numpy.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

draw_params = dict(
                   matchColor       = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask      = matchesMask, # draw only inliers
                   flags            = 2
                   )

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()