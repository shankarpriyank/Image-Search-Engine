# Reverse Image Search Engine

* Reverse Image Search is a Technique in which a Image is being passed as a Input, which act as a query to search for a related images in a database.

* It is a pretty famous way of finding the similar images, images which are equivalent to the given input image, the image will be queried in the database and a set of images related to the input image will be shown.

* The method of reverse image search is being used by the google all across the world.


## Pipeline Architecture

![Blank board](https://user-images.githubusercontent.com/53623244/188302535-990c0ab6-e2cf-4689-b737-dd6549415a33.png)

## End to End Pipeline

### Data Collection
The data consist of the images which are collected through the google, we are utilizing open source image databases which contains the images of large variety.Some open source databases which we have used are Unsplash, flickr.

### Data Wrangling Steps
The dataset consists of the images majorly so we have applied some image transformation, resizing techniques. After fetching the data from S3 bucket we do its processing.

### Model Training
Our solution consists of the two models that are helping to search the image from the Image Database, the first model is ViT-GPT-2 , which is used to generate the captions from the input image and return the caption as a output.

Once after getting the caption is used and feed into another model which is CLIP(Contrastive Learning Image Pretraining) to search for a particular image in the Custom S3 Image Database, and the image similar or equivalent to it will be returned.

### Model Evaluation
For testing the model we have taken a set of images which are scrapped from the google, and feeded into the pipeline where the Custom S3 database is being queried to get the relevant images to it.

### Infra Deployment
The Backend of the Infrastructure is being Dockerized first and then the container is deployed on the AWS EC2 Large Instances. 
The frontend is being deployed on the github pages.

### MLOPS Practices Followed
* The whole backend infra is being deployed onto the AWS EC2 after creating a container of the backend service.
* We have attach Auto Scaling Groups so that our application should not face any downtime at all and it will be available up most of the time.
* The S3 database will act as a single source of datastore, and it will be updated continuously.
* The whole infra is being monitored using AWS cloudwatch.



## Hosted Platform

* The backend is hosted at aws ec2 instance after containarization.
* The frontend is hosted at github pages.

* Backend: http://54.152.25.130:5000

* Frontend: https://nak915.github.io/Reverse-Image-Search-Engine/

* Backend Repo:https://github.com/shankarpriyank/Image-Search-Engine/

* Frontend Repo: https://github.com/NaK915/Reverse-Image-Search-Engine
