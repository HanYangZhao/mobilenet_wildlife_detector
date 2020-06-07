#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.dom
import xml.dom.minidom
import os
import cv2
import json
import argparse
import sys
import multiprocessing
from glob import glob
from os.path import join
from shutil import copy
import numpy as np
import time

parser = argparse.ArgumentParser(description='')
parser.add_argument('--input_json', default='input.json',type=str, help='input json')
parser.add_argument('--image_path', default='images',type=str, help='image path')
args = parser.parse_args()

ann_data = None
img_path = None

_AUTHOR= 'Hujingyuan'
_SEGMENTED= '0'
_DIFFICULT= '0'
_TRUNCATED= '0'
_POSE= 'Unspecified'

def createElementNode(doc,tag, attr):
    element_node = doc.createElement(tag)
    text_node = doc.createTextNode(attr)
    element_node.appendChild(text_node)
    return element_node

def createChildNode(doc,tag, attr,parent_node):
    child_node = createElementNode(doc, tag, attr)
    parent_node.appendChild(child_node)

def createObjectNode(doc,attrs):
    object_node = doc.createElement('object')
    createChildNode(doc, 'name', attrs['name'],
                    object_node)
    createChildNode(doc, 'pose',
                    _POSE, object_node)
    createChildNode(doc, 'truncated',
                    _TRUNCATED, object_node)
    createChildNode(doc, 'difficult',
                    _DIFFICULT, object_node)
    bndbox_node = doc.createElement('bndbox')
    createChildNode(doc, 'xmin', str(int(attrs['bndbox'][0])),
                    bndbox_node)
    createChildNode(doc, 'ymin', str(int(attrs['bndbox'][1])),
                    bndbox_node)
    createChildNode(doc, 'xmax', str(int(attrs['bndbox'][0]+attrs['bndbox'][2])),
                    bndbox_node)
    createChildNode(doc, 'ymax', str(int(attrs['bndbox'][1]+attrs['bndbox'][3])),
                    bndbox_node)
    object_node.appendChild(bndbox_node)
    return object_node

def writeXMLFile(doc,filename,worker_num):
    tmp = 'tmp' + str(worker_num) + '.xml'
    tmpfile =open(tmp,'w')
    doc.writexml(tmpfile, addindent=''*4,newl = '\n',encoding = 'utf-8')
    tmpfile.close()
    fin =open(tmp)
    fout =open(filename, 'w')
    lines = fin.readlines()
    for line in lines[1:]:
        if line.split():
            fout.writelines(line)
    fin.close()
    fout.close()

def multi_processing_xml(sub_list,worker_num,img_path,ann_data):
    print("Worker " + str(worker_num))
    for imageName in sub_list:
        if imageName.split('.')[1] == 'jpg':
            saveName= imageName.strip(".jpg")
            # print(saveName)

            xml_file_name = os.path.join('Annotations', (saveName + '.xml'))

            img=cv2.imread(os.path.join(img_path,imageName))
            # print(os.path.join(img_path,imageName))
            if img is None:
                print("img is empty")
                return
            height,width,channel=img.shape
            # print(height,width,channel)
            img_save_name = os.path.join('Annotations',imageName)

            my_dom = xml.dom.getDOMImplementation()

            doc = my_dom.createDocument(None, 'annotation', None)

            root_node = doc.documentElement
            #print(root_node)
            #input()
            # createChildNode(doc, 'folder', 'COCO'+year, root_node)

            createChildNode(doc, 'filename', saveName+'.jpg',root_node)

            # source_node = doc.createElement('source')

            # createChildNode(doc, 'database', 'LOGODection', source_node)

            # createChildNode(doc, 'annotation', 'COCO'+year, source_node)

            # createChildNode(doc, 'image','flickr', source_node)

            # createChildNode(doc, 'flickrid','NULL', source_node)

            # root_node.appendChild(source_node)

            # owner_node = doc.createElement('owner')

            # createChildNode(doc, 'flickrid','NULL', owner_node)

            # createChildNode(doc, 'name',_AUTHOR, owner_node)

            # root_node.appendChild(owner_node)

            size_node = doc.createElement('size')

            createChildNode(doc, 'width',str(width), size_node)

            createChildNode(doc, 'height',str(height), size_node)

            createChildNode(doc, 'depth',str(channel), size_node)

            root_node.appendChild(size_node)

            # createChildNode(doc, 'segmented',_SEGMENTED, root_node)
            for ann in ann_data:
                if saveName == ann["filename"]:
                    object_node = createObjectNode(doc, ann)
                    root_node.appendChild(object_node)
                    writeXMLFile(doc, xml_file_name,worker_num)
                    copy(os.path.join(img_path,imageName),img_save_name)

def process_xml(imageName):
    saveName= imageName.strip(".jpg")
    print(saveName)

    xml_file_name = os.path.join('Annotations', (saveName + '.xml'))

    img=cv2.imread(os.path.join(img_path,imageName))
    # print(os.path.join(img_path,imageName))
    if img is None:
        print("img is empty")
        return
    height,width,channel=img.shape
    # print(height,width,channel)
    img_save_name = os.path.join('Annotations',imageName)

    my_dom = xml.dom.getDOMImplementation()

    doc = my_dom.createDocument(None, 'annotation', None)

    root_node = doc.documentElement
    #print(root_node)
    #input()
    # createChildNode(doc, 'folder', 'COCO'+year, root_node)

    createChildNode(doc, 'filename', saveName+'.jpg',root_node)

    # source_node = doc.createElement('source')

    # createChildNode(doc, 'database', 'LOGODection', source_node)

    # createChildNode(doc, 'annotation', 'COCO'+year, source_node)

    # createChildNode(doc, 'image','flickr', source_node)

    # createChildNode(doc, 'flickrid','NULL', source_node)

    # root_node.appendChild(source_node)

    # owner_node = doc.createElement('owner')

    # createChildNode(doc, 'flickrid','NULL', owner_node)

    # createChildNode(doc, 'name',_AUTHOR, owner_node)

    # root_node.appendChild(owner_node)

    size_node = doc.createElement('size')

    createChildNode(doc, 'width',str(width), size_node)

    createChildNode(doc, 'height',str(height), size_node)

    createChildNode(doc, 'depth',str(channel), size_node)

    root_node.appendChild(size_node)

    # createChildNode(doc, 'segmented',_SEGMENTED, root_node)
    for ann in ann_data:
        if saveName == ann["filename"]:
            object_node = createObjectNode(doc, ann)
            root_node.appendChild(object_node)
            writeXMLFile(doc, xml_file_name)
            copy(os.path.join(img_path,imageName),img_save_name)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    start = time.time()
    img_path = args.image_path
    fileList = os.listdir(img_path)
    if fileList == 0:
        print("Do not find images in your img_path")
        os._exit(-1)

    with open(args.input_json, "r") as f:
        ann_data = json.load(f)

    current_dirpath = os.path.dirname(os.path.abspath('__file__'))

    if not os.path.exists('Annotations'):
        os.mkdir('Annotations')
    num_proc = multiprocessing.cpu_count()
    print('CPU count: ' + str(num_proc))
    list_of_fileList = np.array_split(fileList,num_proc)
    jobs = []
    for i in range(num_proc):
        p = multiprocessing.Process(target=multi_processing_xml, args=(list_of_fileList[i].tolist(),i,img_path,ann_data))
        jobs.append(p)
        p.start()
    p.join()

    # end time
    end = time.time()

    # total time taken
    print(f"Runtime of the program is {end - start}")