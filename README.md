# Analysis of US Opioid Trends Using SIR Models, Stochastic Process, and Machine Learning

## Project Goal

This project was submitted as part of the Mathematical Contest in Modeling 2019. It aims to describe and implement several mathematical approaches toward analyzing properties of the US Opioid Crisis, a huge drug-related problem that is prevalent in the US. Because these models were merely created within a couple days, we only analyzed 5 of the 50 US states. Our analysis aimed to accomplish two goals:

1. Given the number of opioid/heroin identification cases for the counties in each US state per year, we want use the data to backtrack to which county was the original main source of these drugs.

2. Given various statistics from the US Census Bureau (ex. household numbers, marriage, ancestry, education level) on each county in the 5 US states, we want to figure out which factors are highly correlated to increased opioid use. If any of the factors are a potential reason for high drug trade, we also aim to find reasons why the factors influence the drug trade.

### Prerequisites

- Python 3.6+
- Jupyter Notebook
- ```requirements.txt``` provides Python dependencies

## Overview of the Paper and Models

The paper describes the different models and methods we used. 

### Finding the "source" county of drug trade in each state:

1. **SIR Model**: inspired by a system of differential equations that interact with one another. Each differential equation is defined (high level) as:
>> * those who are *susceptible* to heroin abuse  
>> * those who are *involved* in heroin abuse 
>> * those who are in *recovery* from heroin abuse (or moved out of the county)

2. **CountyRank Model**: inspired by the Page Rank Algorithm (originally used by Google Search)

3. **Markov-based Model**: inspired by Markov Chains and process-of-elimination backtracking to find the source node

### Determining the significant factors relating to drug trade in each state (ML):

1. **SVM Classifier** (poly kernel): Given filtered statistics on a county, it classifies the county as having "high" or "low" opioid activity, where "high" and "low" based on a threshold (hyperparameter). Thresholds closer to the median (out of counties tested in the training data) have been tested to give higher accuracy rates (~95%).

2. **Random Forest Regressor/Classifier**: An alternative approach to SVM. Given filtered statistics on a county, it attempts to predict what range of drug activity level the county would belong to. The advantage of this over the SVM is that taking the decision trees from the forest allows us to see which factors are most impactful in the data set.
>> * The **regressor** predicts precisely the drug activity level the county would have. However, given the high variance of the data across many features, this has given bad out-of-bag scores.
>> * The **classifier** predicts the range of drug activity level the county would belong to. This is more accurate than the regressor, but still not quite accurate, due to high variance in data and more classes compared to SVM.

## Execution

### Running the Models

- ```Models/*.py``` files are non-machine learning models can be run directly with Python.
- ```Models/*.ipynb``` files are machine learning models that must be run with Jupyter.

### Running the Scripts

- Scripts can be run with Python, located in ```scripts/*.py``` 

## Authors

* **Tanishq Bhatia** - *Implementor of SIR model, CountyRank model, scripts, plots* - [Tanishqbh](https://github.com/Tanishqbh)
* **Clayton Chu** - *Implementor of Markov-based model, SVM, Random Forest, cleaning data, scripts* - [pacbac](https://github.com/pacbac)
* **Jerry Yin** - *Main creator of models, writing the paper (and almost everything part of it)* - [JerryYinUCLA](https://github.com/JerryYinUCLA)
