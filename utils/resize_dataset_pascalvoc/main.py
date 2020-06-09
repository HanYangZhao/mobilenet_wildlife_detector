import os
import argparse
from image import process_image
from utils import create_path, add_end_slash
import multiprocessing
import numpy as np

IMAGE_FORMATS = ('.jpeg', '.JPEG', '.png', '.PNG', '.jpg', '.JPG')


def multiprocess_image(root,files,output_path,x,y,save_box_images):
    for file in files:
        if file.endswith(IMAGE_FORMATS):
            file_path = os.path.join(root, file)
            process_image(file_path, output_path, int(x),int(y), save_box_images)




parser = argparse.ArgumentParser()

parser.add_argument(
    '-p',
    '--path',
    dest='dataset_path',
    help='Path to dataset data ?(image and annotations).',
    required=True
)
parser.add_argument(
    '-o',
    '--output',
    dest='output_path',
    help='Path that will be saved the resized dataset',
    default='./',
    required=True
)
parser.add_argument(
    '-x',
    '--new_x',
    dest='x',
    help='The new x images size',
    required=True
)
parser.add_argument(
    '-y',
    '--new_y',
    dest='y',
    help='The new y images size',
    required=True
)
parser.add_argument(
    '-s',
    '--save_box_images',
    dest='save_box_images',
    help='If True, it will save the resized image and a drawed image with the boxes in the images',
    default=0
)


if __name__ == "__main__":
    args = parser.parse_args()

    create_path(args.output_path)
    create_path(''.join([args.output_path, '/boxes_images']))

    args.dataset_path = add_end_slash(args.dataset_path)
    args.output_path = add_end_slash(args.output_path)

    for root, _, files in os.walk(args.dataset_path):
            output_path = os.path.join(args.output_path, root[len(args.dataset_path):])
            create_path(output_path)


            num_proc = multiprocessing.cpu_count()
            print('CPU count: ' + str(num_proc))
            list_of_fileList = np.array_split(files,num_proc)
            jobs = []
            print(len(list_of_fileList[0]))
            for i in range(num_proc):
                p = multiprocessing.Process(target=multiprocess_image, args=(root,list_of_fileList[i].tolist(),output_path,args.x,args.y,args.save_box_images))
                jobs.append(p)
                p.start()
            p.join()

            # for file in files:
            #     if file.endswith(IMAGE_FORMATS):
            #         file_path = os.path.join(root, file)
            #         process_image(file_path, output_path, int(args.x),int(args.y), args.save_box_images)
