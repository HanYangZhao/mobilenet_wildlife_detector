# What is it?

This repo contains a neural network model to detect animals from video or images. It is similar to the Faster-RCNN + InceptionResNetv2 architecture. This way, it can be used with TFLite as well as the Coral TPU Acccelerator since Faster-RCNN is not supported as of June 2020 in TFLite. Of course the accuracy will not be as good as the megadetector, but the inference speed is much faster. It was trained using the [ENA-24](http://lila.science/datasets/ena24detection) dataset using transfer learning (only the last few layers of the Mobilenet is trained). 

# How to use
## Pre-requisite

* Pre-req for opencv

	```
	sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
	sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
	sudo apt-get -y install libxvidcore-dev libx264-dev
	sudo apt-get -y install qt4-dev-tools libatlas-base-dev
	```

* python3
* pensorflow (either 2.x or 1.15)
* picamera (if using Picam)
* opencv-python
* numpy

## Inference 
* Install TF-Lite runtime
	* Follow the instructions [here](https://www.tensorflow.org/lite/guide/python)
	* Install software for [EdgeTPU](https://coral.ai/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime)
	* If you're using a RPI without the EdgeTPU, consider [this](https://github.com/PINTO0309/TensorflowLite-bin) alternative TF-Lite runtime for faster inference

* In your clone repo

	```
	cd infer
	wget https://github.com/HanYangZhao/mobilenet_wildlife_detector/releases/download/1/model.zip
    unzip model.zip
    ```

    * For testing with video
    ```
    python3 TFLite_detection_video.py --modeldir model/ --video night.mp4 --edgetpu
    ```

    * For testing with stream
    ```
    python3 TFLite_detection_video.py --modeldir model/ --stream_url 'http://....' --edgetpu
    ```

	* For testing with webcam
	```
	python3 TFLite_detection_webcam.py --modeldir model/
	```

    Remove the ```--edgetpu``` flag if not using the coral edgetpu

## Training

Use the provided google colab notebook to perform training. The training will use the tfrecord from [here](https://github.com/HanYangZhao/mobilenet_wildlife_detector/releases/download/1/wildlife.v3.tfrecord.zip). The tfrecords aggreated all the difference classes of animals into one 'Animal' class. Because the mobilnet architecture doesn't  classify the different classes of animals accurately. In total there are 3 classes : Animals, Humans, Vehicle.


The downsized (300x300) and pascal-voc annotated ENA-24 iamges can be downloaded [here](https://github.com/HanYangZhao/mobilenet_wildlife_detector/releases/download/1/ena24_small.zip)
The ```utils``` folder contains tools to convert the images dowloaded from lila.science to TFrecords that can be used for training

## Acknolegements

Many thanks to [EdjeElectronics](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md) as well as the people at lila.science

The training script is adapted from [here](https://towardsdatascience.com/custom-object-detection-using-tensorflow-from-scratch-e61da2e10087) and from [PINTO0309](https://github.com/PINTO0309/TPU-MobilenetSSD/tree/master/colaboratory/gpu)

