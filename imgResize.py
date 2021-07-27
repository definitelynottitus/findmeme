import cv2, sys, os

if len(sys.argv) < 3:
    print("please provide image path[2] and the desired save path[1]")
    exit()

if not os.path.isdir(sys.argv[1]):
    print('invalid input file path for saving destination')
    exit()

for i,f in enumerate(sys.argv[2:]):
    print(f'resizing file {i}: {f}')
    try:
        img = cv2.imread(f)
        img = cv2.resize(img,(255,255))
        cv2.imwrite(f'{sys.argv[1]}/{i}.png',img)
    except Exception as error:
        print(f'Invalid path or image format: {error}')