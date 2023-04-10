# Exercise 1 - Language Detection 

This project provides a REST API to detect if the language of a given sentence is in Italian or not. The application is based on a classifier trained on a dataset of text samples from 17 different languages, which can be found on [Kaggle](https://www.kaggle.com/datasets/basilb2s/language-detection).

The project is divided into three main components:

- **Language_detection.ipynb**: A Jupyter notebook, available also on [Google Colab](https://colab.research.google.com/drive/1cdAb12xi1M4Ly-Dzpo3f3c-7BpCsFgdc?usp=sharing), used to analyze the Kaggle dataset, preprocess the text data, and perform a grid search to choose the optimal vectorizer and classifier. The fitted model is then saved as a pickle file (language_detection_model.pkl) which can be found in the *model* folder.

- **REST_API.py**: A Python script containing the FastAPI implementation of the REST API. The API accepts POST requests with a JSON body containing a single sentence to classify, and returns a JSON response with the predicted language, 1 for Italian sentences and 0 for Non-Italian sentences. The static folder contains the ui.html file and style.css file used to display a simple web interface for the REST API.

- **Dockerfile**: A Docker file used to build and run a Docker container that runs the REST API. The API will operate at **http://localhost:5000**.

## Usage
To use the API, you can either run it using Docker or directly using Python (we tested the build on a Windows machine and provided the Docker image to avoid any issues with other platforms, therefore if you are a non-Windows user, we suggest you to download the Docker image to avoid compatibility problems).

### Running with Docker
You can download the Docker image from [Docker Hub](https://hub.docker.com/repository/docker/christianbrignone/language-detection/general) or alternatively build the Docker image yourself
- Download the Docker image
  - Download the Docker image: `docker pull christianbrignone/language-detection:latest` 
  - Run the Docker container: `docker run -p 5000:5000 christianbrignone/language-detection`
- Build the Docker Image
  - Clone this repository: `git clone https://github.com/ChristianBrignone/LanguageDetection.git`
  - Navigate to the root directory of the project: `cd LanguageDetection`
  - Build the Docker image: `docker build -t language-detection . `
  - Run the Docker container: `docker run -p 5000:5000 language-detection`

### Running with Python
- Clone this repository: `git clone https://github.com/ChristianBrignone/LanguageDetection.git`
- Navigate to the root directory of the project: `cd LanguageDetection`
- Install the required Python packages: `pip install -r requirements.txt`
- Start the REST API server: `python REST_API.py`


### POST requests
#### curl
Once the API is running, either with python or Docker, you can send a POST request to http://localhost:5000/predict with a JSON body containing a single sentence to classify by using the following line:

```
 curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"This is an example sentence to classify.\"}"  http://localhost:5000/predict
```

This will return a **JSON** response with the predicted language:

> {"prediction": 0}

Note that if you would like to classify sentences containing special characters like *è*, *ç* and *ì* you may get an error **400 Bad Request**.
To avoid this, you can use the [Unicode escape sequence](https://dencode.com/string/unicode-escape) for the corresponding character. 
For example, if we want to classify the sentence *"questa è una frase in italiano!"*, we need to replace the character *"è"* with  *"\u00E8"* like in the following:

```
curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"questa \u00E8 una frase in italiano!\"}" http://localhost:5000/predict
```

In alternative, you can also employ a **JSON** file containing the data and use the following command without replacing the sentence's special characters.
Infact, by using the **payload.json** file containing
```
{"text": "questa è una frase in italiano!"} 
```
and the following **curl** command
```
curl -X POST -H "Content-Type: application/json" --data-binary "@payload.json" http://localhost:5000/predict
```
we will get
> {"prediction": 1}

The API documentation can be found [here](http://localhost:5000/docs).

#### User interface

In addition, for those who prefer a graphical interface, we have also provided a simple [user interface](http://localhost:5000) to facilitate the use of the API. 
By using the graphical interface we also avoid the problems related with the special characters, therefore you can simply write a sentence in the form and predict its class by using the *Predict* button.

## Model

To create the model, we began by analyzing the dataset and cleaning the text. 

Next, we used a grid search to select the best tokenizer, vectorizer, classifier, and their hyperparameters employing 5-fold cross-validation and F1 score as the evaluation metric. 

The grid search led us to a pipeline composed of a word-level bigrams tokenizer, a count vectorizer and a multinomial naive Bayes with alpha=0.1.

We evaluated the model performance on the test set by using several evaluation metrics (accuracy, precision, recall and F1-score). Our final model achieved excellent results with an F1-score of 0.993. 

The trained model was then saved using *pickle* and is loaded in the REST API to make predictions.

To have a clearer picture of the motivations and implementational choices, please, refer to the [Language_detection.ipynb](https://colab.research.google.com/drive/1cdAb12xi1M4Ly-Dzpo3f3c-7BpCsFgdc?usp=sharing) notebook.

## Improvements

Possible improvements of this work, in the case in which we would have more resources at our disposal (dataset size, time, computational power ect.), can be various. First of all, in presence of a large dataset, possibly containing more languages, and considering the possibility of having access to the necessary computing power, the choice of the model would be different, for example we may employ the pretrained XLM-RoBERTa architecture and apply a fine-tuning on our data.

Another aspect that can be expanded, is the implementation of the REST API. In fact, to mantain the application as simple as possible to meet the requirement (inference call which should return 1 for Italian and 0 for a Non-Italian sentence), many aspects have been simplified, like the possibility to detect multiple senteces simultaneously, an authentication mechanisms and a better managment of the stats codes.

# Exercise 2 - Machine Translation

The anwsers to the questions can be found if the file named **Exercise2.pdf**.