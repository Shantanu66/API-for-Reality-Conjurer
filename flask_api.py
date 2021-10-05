from flask.app import Flask
import tensorflow as tf
from keras.models import load_model
from flask import flash,jsonify,request
import base64
import io
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import time
from keras.preprocessing.image import save_img
import time
from flask_restful import Resource,Api,reqparse
#basic idea here is to fetch the image from flutter appp
#in json format and encode it in base64 format and then
#call MakeImage Function to resize and then 

#instantiate a flask server
app=Flask(__name__)
api=Api(app)


model=load_model('test.h5')
print("* model loaded")


def MakeImage(image,target):
    if image.mode!="RGB":
        image=image.convert("RGB")
    image=image.resize(target)
    #convert image to array for representaion of the image 
    #in numbers
    image=img_to_array(image)
    #for normalizing the the image for ease in training
    #the model
    image=(image - 127.5)/127.5
    #expand the dimension of the image
    image=np.expand_dims(image,axis=0)
    #return preprocessed image
    return image


class PredictFace(Resource):
    def postData(self):
        #getting the image from flutter application
        json_data=request.get_json()
        #json data key string pair
        img_data=json_data['Image']

        #decoding the image from baase64
        image=base64.b64decode(str(img_data))
        #make final image
        img=Image.open(io.BytesIO(image))
        #send the image for changes according to the neural 
        # network
        preparedImage=MakeImage(img,target=(256,256))

        #Predict the image section

        #so now pred is our generated image
        #we predict the image output by passing the
        #basically the model contains all the predicted images in
        #the nueral network that we have trained in collab
        #it now basically contains all the predicted images
        #with the reference image and the sketch
        #so we now load that model using keras in vscode
        #and we predict the what prepared image(output) we will get 
        #based on the sketch(preparedImage) that we pass as 
        #argument
        pred=model.predict(preparedImage)

        #now we need a way to send back the data

        #firstly save the preprocessed image in an output folder
        outputfile="output.png"
        savePath="./output/"
        
        #now we need to reshape our predicted image
        output=tf.reshape(pred,[256,256,3])
        #renormalize it
        output=(output+1)/2
        #save the image in output folder
        save_img(savePath+outputfile,img_to_array(output))
        #open the image
        imageNew=Image.open(savePath+outputfile)
        #resize the image again as we cant send too much data
        #through the flask backend so compress it
        imageNew=imageNew.resize((50,50))
        #save the new resized image
        imageNew.save(savePath+"new_"+outputfile)
        #now opening it 
        with open(savePath+"new_"+outputfile,'rb') as image_file:
            #now encoding the string into base64
            encoded_string=base64.b64encode(image_file.read())
        #now we can send our data back in json format
        #therefore encoding was required
        #create a json data
        #with key as image and value as string base64image
        #typecasting with string to mantain scalibility
        outputData={'Image':str(encoded_string) } #for scalibitltiy

        return outputData

api.add_resource(PredictFace,'/predict')
if __name__=='__main__':
    app.run(debug=True)

#sucessfully created an api for interaction of client and server





        


