# Language Detection 

This project provides a REST API to detect if the language of a given sentence is in Italian or not. The application is based on a Naive Bayes classifier trained on a dataset of text samples from 17 different languages, which can be found on [Kaggle](https://www.kaggle.com/datasets/basilb2s/language-detection).

The project is divided into three main components:

- **Language_detection.ipynb**: A Jupyter notebook used to analyze the Kaggle dataset, preprocess the text data, and perform a grid search to choose the optimal vectorizer and classifier. The fitted model is then saved as a pickle file (language_detection_model.pkl) which can be found in the *model* folder.

- **REST_API.py**: A Python script containing the FastAPI implementation of the REST API. The API accepts POST requests with a JSON body containing a single sentence to classify, and returns a JSON response with the predicted language, 1 for Italian sentences and 0 for Non-Italian sentences. The static folder contains the ui.html file and style.css file used to display a simple web interface for the REST API.

- **Dockerfile**: A Docker file used to build and run a Docker container that runs the REST API. The API will operate at **http://localhost:5000**.

## Usage
To use the API, you can either run it using Docker or directly using Python.

### Running with Docker
- You can download the Docker image from [Docker Hub]() or alternatively build the Docker image yourself with the following lines: 
  - Clone this repository: `git clone https://github.com/ChristianBrignone/LanguageDetection.git`
  - Navigate to the root directory of the project: `cd LanguageDetection`
  - Build the Docker image: `docker build -t language-detection . `
- Run the Docker container: `docker run -p 5000:5000 language-detection`

### Running with Python
- Clone this repository: `git clone https://github.com/ChristianBrignone/LanguageDetection.git`
- Navigate to the root directory of the project: `cd LanguageDetection`
- Install the required Python packages: `pip install -r requirements.txt`
- Start the REST API server: `python REST_API.py`

Once the API is running, either with python or Docker, you can send a POST request to http://localhost:5000/predict with a JSON body containing a single sentence to classify. 

For example, using curl:

```
 curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"This is an example sentence to classify.\"}"  http://localhost:5000/predict
```

This will return a JSON response with the predicted language:

> {"prediction": 0}

In addition, for those who prefer a graphical interface, we have also provided a simple [user interface](http://localhost:5000) to facilitate the use of the API.

## Model

To create the model, we began by analyzing the dataset and cleaning the text. 

Next, we used a grid search to select the best tokenizer, vectorizer, classifier, and their hyperparameters employing 5-fold cross-validation and F1 score as the evaluation metric. 

The grid search led us to a pipeline composed of a word-level bigrams tokenizer, a count vetctorizer and a multinomial naive bayes with alpha=0.1.

We evaluated the model performance on the test set by using several evaluation metrics (accuracy, precision, recall and F1-score). Our final model achieved excellent results with an F1-score of 0.993. 

The trained model was then saved using *pickle* and is loaded in the REST API to make predictions.

To have a clearer picture of the motivations and choices, please, refer to the **Language_detection.ipynb** notebook.