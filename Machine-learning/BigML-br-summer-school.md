# BigML - Brazilian Summer School
Notes from the BigML Brazilian Summer School training on Nov. 27th 2017

### What is ML?
Replace the expert with data...
1. Get data (lots of it)
2. Apply ML
3. Generate a model to predict

"A field of study that gives computers the ability to learn without being explicitly programmed." Arthur Samuel, 1959

### Intuitive Statistics
Simpson's paradox: a trend that appears in different groups of data disappears when...

## What can ML answer?
|Question|Model Resource|
|---|---|
|Will this customer default on a loan|Models / Esembles / Deepnets / LR|

### Mythical ML Model?
- High representational power
- High ease-of-use
- Ability to work with real-world data

## ML Definition
- The computer learns from examples, that is data
- The programa is the creation of a model
- The model as the ability to answer a question about new inputs similar to the training data

## ML: Two Methods
|Supervised|Unsupervised|
|---|---|
|Rquires labelled data|Does not require labelled data|
|Goal is to predict the label often called the objective|Goal is "discovery", with algorithms focused on type|
|Can be evaluated against the label|Each algorithm has it's own quality measures|
|Models/ensembles, LR, deepnets, time series|Clustering, anomaly detection|

### Supervisioned learning
- If the label is numeric: regression
- If the label is categorical: classification / Multi-label classification

#### Decision Trees
Why use it?
- Works for classification and regression
    - For non-linear regression, discretize label Y, splits on feature X, the predicted values are the average
- Easy to understand: splits are features and values
- Lightweight and super fast at prediction time
- Relatively parameter free
- Data can be messy
    - Useless features are automatically ignored
    - Works with un-normalized data
    - Works with missing data (training and prediction)
    - Resilient to outliers
- High representational power
- Works easily with mixed data types

Why not use DT?
- Slightly prone to over/under-fitting
    - Under-fitting
        - Model does not fit well enough
        - Does not capture the underlying trend of the data
        - Change algorithm or features
    - Over-fitting (can be fixed with ensembles)
        - Model fits too well does not "generalize"
        - Captures the noise or outliers of the data
        - Change algorithm or filter outliers
- Splitting prefers decision boundaries that are parallel to feature axes

## Weighting
Some variables / values are more important to our model

## Evaluation
We need metrics to evaluate our model
- Metrics: select your positive class (the one you want to predict), use the model on your test set and check for:
    - True Positive = 
    - True Negative = 
    - False Positive = said it was positive, but wasn't 
    - False Negative = 
- Accuracy
    - (TP + TN) / Total
    - "Percentage correct" - like an exam
    - = 1 then no mistakes
    - = 0 then all mistakes
    - Intuitive but not always useful
    - Watch out for unbalanced classes!
- Precision
    - TP / (TP + FP)
    - Accuracy or purity of positive class
    - How well you did separating the positive class from negative class
    - Precision = 1 then no FP
- Recall
    - TP / (TP + FN)
    - Percentage of positive class correctly identified
    - A measure of how well you identified all of the positive class examples
    - Recall = 1 then no FN > All left handers identified
    - Recall = 0 then

- f-Measure
    - (2 * Recall * Precision) / (Recall + Precision)
    - Harmonic mean of recall & precision
    - If = 1 then recall == precision == 1

- Pfi Coefficient
    - ((TP * TN) - (FP * FN)) / ...


**Important**
- Never evaluate with the training data!
    - Many models are able to memorize the training data
    - This will result in overly optmistic evaluations
- Even a train/test split may not be enough
- Don't forget that accuary can be mis-leading

##
- MSE - Mean squared error
- MAE - Mean absolute error
- R-Squared Error
    - 1 - (MSE model / MSE mean)
    - Measure of how much better the model is than always predicting the mena
    - < 0 model is worse then mean
    - = 0 model is no better than the mean
    - -> 1 (close to one) model firts the data "perfectly"

## Ensemble
No model is perfect:
- A given ML algorithm may simply **not be able** to exactly model the "real situation"of a particular dataset.
- Even if the model is very capable, the "real slution" may be elusive
- No data is perfect
    - No enough, we are always working with finite training data
- Anomalies / outliers
- Mistakes in your data

**Key idea**
- By combining several good "models, the combination may be closer to the best possible "model"
- Training data tricks
    - Build several models each with only some of the data
    - Introduce randomness directly into the algorithm
    - Add training weights to "focus" the additional models on the mistakes made
- Pediction tricks
    - Model the mistakes
    - Model the output with other algorithms

## Decision forest
We simply create different models with different subsets of the dataset. After that we make predictions using the models and use a combiner to result in a unique prediction.
- Individual tree parameters are still available
- Number of models: how many trees to build
- Sampling options:
    - Deterministic / Random
    - Replacement:
        - Allows sampling the same instance more than once
        - Effectively the same as ~ 63.21%
        - "Full size"samples with zero covariance (good thing)
- At prediction time
    - Combiner...

Combiners:
- Regression: average of the predictions and expected error
- Classification:
    - Plurality: majority wins
    - ...

## Random Decision Forest (RDF) 
It gets an dataset and generate subsets getting random rows and features (columns/variables).

## Bootsting
It's a process
- Build a model
- Make a prediction
- Measure the error
- Create a new dataset using the error
- Build a model for the error
- Use both models, one to predict your goal and the other to predict the error of the model
- You can keep doing this for each model
- At the end you summarize the results and get a final prediction

### Boosting Config
- Number of iterations: similar to number of models for DF/RDF
- Iterations com be limited with Early Stopping
    - Early ou of bag
    - Early holdout: tests with a portion
    - None
- Learning Rate
- You can combine sampling with Boosting

### What about classification?
- You can change the categorical values for numbers if they are binary
- With multiple classes you need to create a model for each class (A, NOT-A), and repeat it for each model, using probability

## Which Ensemble method to use?
- The one that works best!
- For large/complex datasets
    - Use DF / RDF with deeper node threshold
- For "noisy" data
    - Boosting may overfit
    - RDF preferred
- For "wide" (lots of features)
    - A RDF will be quicker
- For "easy"
    - A single model may be fine
- For classification with large number of classes
    - Boosting will be slower
- For "general"data
    - DF/RDF

## Too many parameter?
- How many tress
- SMACdown!

## Stacked generalization
TODO...

## Comparison
|LR|DT|
|---|---|
|Expects a smooth relationship with predictors|Adapts well to ragged non-linear relationships|
|LR is concerned with probability of a discrete outcome|Non concer: classification, regression, multi-class all fine|
|Lots of parameters to get wrong: regularization||

## Deepnet
- What is?
    - Supervised learning algorithm
    - Classification and regression
    - LR leveled up
- What isn't?
    - A Convolutional Neural Network
    - Recurrent Neural Network or LTSM
        - These are special architectures that are adept at NLP and speech recognition
    - The last ML algorithm you will ever need...

### Why deepnets?
- Trees
    - Pro:
    - Con:
- LR
    - Pro: some smooth, multivatiate, functions are not a proble, fast optimization
    - Con: parametric
- Like trees / Ensembles, we have arbitrary representational power by modifying the structure
- What have we lost?
    - Interpretability
    - Ease of use
    - Most structures are bad

**Metalarning**

### When to use DP
- When the absolute best performance is worth the computational time
- When you willing to wait to be more accurate (ex: predicting cancer vs predicting churn)

### When not to use DP
- When you have small data (could still be thousands of instances)
- As a first model - start with something simpler
- Feature engineering always beats model selection
- Problems that are easy or where retraining often

*Remember deep learning is just another sort of supervised learning algorithm*

## Data Types
- Numeric
- Categorical
- Date-time
- Text / items


## Logistic Regression
*Logistic regression is a classification algorithm... that uses a regression... to model the probability of the discrete objective*

*Regression is the process of "fitting" a function to the data* 
- Linear regression
- Quadratic regression
- Decision Tree regression

**What if we want to do a classification for a binary (1/0, tru/false)?**
- Logistic function

### Interpreting coefficients
- LR computes B0 and coefficients B1 for each feature Xj
    - Negative Bj -> negative correlated: Xj /\ then P(X) \/
    - ...
- Can include a coefficient for "missing"

## Important infomartion about your dataset and model
### Show statistics for each field on your dataset
- Count
- Missing
- Histogram
    - How you do this for text field?
### Show your model evaluation
- Accuracy
- Precision
- Recall
- F-measure
- Phi-coefficient

