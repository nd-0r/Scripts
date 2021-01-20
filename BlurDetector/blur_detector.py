import cv2
import argparse
import glob

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', nargs='+', required=True)
ap.add_argument('-t', '--threshold', type=float)
args = vars(ap.parse_args())
print(args['images'])

images = [cv2.imread(file) for file in args['images']]

for image in images:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()

    if fm < args["threshold"]:
        print("blurry")