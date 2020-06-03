#! /usr/bin/env python
#-*-coding=utf-8 -*-
import argparse
import json
import sys

def parse_args():
    desc = "something"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input_json', type=str, default='input.json', help='json metadata')
    parser.add_argument('--output_json',type=str, default='output.json', help='output json')
    return parser.parse_args()

def writeNum(Num,output):
    with open(output,"w") as f:
        f.write(str(Num))


if __name__ == '__main__':
    args = parse_args()
    if args is None:
        print("error")
        exit()

    className = {
                0:'Bird',
                1:'Eastern Gray Squirrel',
                2:'Eastern Chipmunk',
                3:'Woodchuck',
                4:'Wild Turkey',
                5:'White_Tailed_Deer',
                6:'Virginia Opossum',
                7:'Eastern Cottontail',
                8:'Human',
                9:'Vehicle',
                10:'Striped Skunk',
                11:'Red Fox',
                12:'Eastern Fox Squirrel',
                13:'Northen Raccoon',
                14:'Grey Fox',
                15:'Horse',
                16:'Dog',
                17:'American Crow',
                18:'Chicken',
                19:'Domestic Cat',
                20:'Coyote',
                21:'Bobcat',
                22:'Ameican Black Bear'
                }

    classNum = [0,1,2,3,7,8,9,10,11,12,13,14,15,19,20,21]


    inputfile = []
    inner = {}

    with open(args.input_json,"r+") as f:
        allData = json.load(f)
        data = allData["annotations"]

    for i in data:
        if(i['category_id'] in classNum):
            inner = {
                "filename": i["image_id"],
                "name": className[i["category_id"]],
                "bndbox":i["bbox"]
            }
            inputfile.append(inner)
    inputfile = json.dumps(inputfile)
    writeNum(inputfile,args.output_json)
