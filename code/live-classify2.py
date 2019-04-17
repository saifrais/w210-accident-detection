import tensorflow as tf
import sys
import os
import cv2
import math

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'



label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("/Users/matthewpotts/Google Drive/UCBerkeley/w251/Final Project/retrained_labels.txt")]

with tf.gfile.FastGFile("/Users/matthewpotts/Google Drive/UCBerkeley/w251/Final Project/retrained_graph.pb", 'rb') as f:

    graph_def = tf.GraphDef()	## The graph-graph_def is a saved copy of a TensorFlow graph;
    graph_def.ParseFromString(f.read())	#Parse serialized protocol buffer data into variable
    _ = tf.import_graph_def(graph_def, name='')	# import a serialized TensorFlow GraphDef protocol buffer, extract objects in the GraphDef as tf.Tensor

	#https://github.com/Hvass-Labs/TensorFlow-Tutorials/blob/master/inception.py

with tf.Session() as sess:

	video_capture = cv2.VideoCapture(0)

    #video_capture = cv2.VideoCapture(0)

	#frameRate = video_capture.get(5) #frame rate
	i = 0
	while True:  # fps._numFrames < 120
		frame = video_capture.read()[1] # get current frame
		frameId = video_capture.get(1) #current frame number
		#if (frameId % math.floor(frameRate) == 0):
		if (0 == 0):  # not necessary
			i = i + 1
			cv2.imwrite(filename="screens/"+str(i)+"alpha.png", img=frame); # write frame image to file
			image_data = tf.gfile.FastGFile("screens/"+str(i)+"alpha.png", 'rb').read() # get this image file
			softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
			predictions = sess.run(softmax_tensor, \
					 {'DecodeJpeg/contents:0': image_data})		# analyse the image
			top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
			for node_id in top_k:
				human_string = label_lines[node_id]
				score = predictions[0][node_id]
				print('%s (score = %.5f)' % (human_string, score))
			print ("\n\n")
            cv2.putText(frame,'%s (score = %.5f)' % (human_string, score),(10,500), font, 1,(255,255,255),2)
			cv2.imshow("image", frame)  # show frame in window
			cv2.waitKey(1)  # wait 1ms -> 0 until key input

	video_capture.release() # handle it nicely
	cv2.destroyAllWindows() # muahahaha
