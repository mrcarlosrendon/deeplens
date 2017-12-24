import sys
import cv2
import awscam


if (not len(sys.argv) == 2):
    print("Usage: [outfile name]")
    exit(1)

ret, img = awscam.getLastFrame()
cv2.imwrite(sys.argv[1], img)
