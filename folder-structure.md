### Project Structure

```plaintext
credit-card-fraud-detection-project
├── api_engine/
│   ├── __pycache__/
│   │   ├── __init__.cpython-311.pyc [204 bytes]
│   │   └── main.cpython-311.pyc [1.77 KB]
│   ├── Dockerfile [274 bytes]
│   ├── __init__.py [0 bytes]
│   └── main.py [879 bytes]
├── app_ui/
│   ├── templates/
│   │   └── index.html [2.09 KB]
│   ├── Dockerfile [156 bytes]
│   ├── __init__.py [0 bytes]
│   ├── app.py [1.12 KB]
│   └── requirements.txt [15 bytes]
├── config/
│   └── config.yaml [340 bytes]
├── data/
│   ├── bi/
│   │   └── predictions.csv [9.68 MB]
│   ├── processed/
│   └── raw/
│       └── fraudTest.csv [132.96 MB]
├── kafka/
│   ├── consumer.py [1.44 KB]
│   └── producer.py [1.11 KB]
├── mlruns/
├── models/
│   ├── encoding_maps.pkl [55.99 KB]
│   ├── model.pkl [288.17 KB]
│   ├── threshold.pkl [117 bytes]
│   └── train_columns.pkl [987 bytes]
├── notebooks/
│   └── model_training.ipynb [186.50 KB]
├── src/
│   ├── __pycache__/
│   │   └── __init__.cpython-311.pyc [197 bytes]
│   ├── feature_engineering/
│   │   ├── __init__.py [0 bytes]
│   │   └── features.py [1.29 KB]
│   ├── ingestion/
│   │   ├── __init__.py [0 bytes]
│   │   └── data_loader.py [80 bytes]
│   ├── model/
│   │   ├── __init__.py [0 bytes]
│   │   ├── evaluate.py [545 bytes]
│   │   ├── predict.py [0 bytes]
│   │   └── train.py [879 bytes]
│   ├── pipeline/
│   │   ├── __pycache__/
│   │   │   ├── __init__.cpython-311.pyc [206 bytes]
│   │   │   ├── examine.cpython-311.pyc [754 bytes]
│   │   │   ├── inference_pipeline.cpython-311.pyc [4.44 KB]
│   │   │   └── training_pipeline.cpython-311.pyc [9.77 KB]
│   │   ├── __init__.py [0 bytes]
│   │   ├── examine.py [471 bytes]
│   │   ├── inference_pipeline.py [1.96 KB]
│   │   └── training_pipeline.py [2.61 KB]
│   ├── preprocessing/
│   │   ├── __init__.py [0 bytes]
│   │   └── preprocess.py [359 bytes]
│   ├── utils/
│   │   ├── __init__.py [0 bytes]
│   │   ├── config.py [0 bytes]
│   │   ├── exception.py [0 bytes]
│   │   ├── helpers.py [0 bytes]
│   │   └── logger.py [0 bytes]
│   └── __init__.py [0 bytes]
├── Dockerfile [0 bytes]
├── docker-compose.yml [1.42 KB]
├── requirements.txt [93 bytes]
└── setup.py [1.18 KB]
```


### Summary

```plaintext
Root Folder: credit-card-fraud-detection-project
Total Folders: 22
Total Files: 49
File Types:
  - .yml Files: 1
  - No Extension Files: 3
  - .txt Files: 2
  - .py Files: 27
  - .pyc Files: 7
  - .html Files: 1
  - .yaml Files: 1
  - .csv Files: 2
  - .pkl Files: 4
  - .ipynb Files: 1
Largest File: fraudTest.csv [132.96 MB]
Smallest File: Dockerfile [0 bytes]
Total Project Size: 143.20 MB
Ignored Files and Folders:
  - venv
```
