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

## What is time series?
- Traditional machine learning data is assumed to be independent & identically distributed
    - Independent
    - Identically distributed: come form the same distribution

## Exponential smoothing
**Idea**: each new value in the series depends on all previous values with a decaying weight

**Problem**:

**Trend**: a persistent long-term pattern
- Additive
- Multiplicative

**Seasonality**: a recurring shorter-term pattern
- Additive
- Multiplicative

**Error**: cumulative error from the smoothing
- Additive
- Multiplicative

***These can all be modeled with time series as weel!***

## Time Series Evaluation
TODO

# Unsupervised Learning
## Clustering
- Is an unsupervised learning technique
- No labels necessary
- Useful to find similar instances
- Finds "self-similar"groups of instances
- Defines each group by a "centroid"

### Useful for
- Customer segmentation
- Similarity
- Active learning
    - Rather than sample randomly, use clustering to group by similarity and then test a sample for each group
- Item discovery

## K-means Algorithm
- Find "best"

## K++ initial centers
- k++

## Finding K: G-Means

## Anomaly Detection
- An unsupervised learning technique
- Find instances that do not matcg
- Defines each unusual instance by an "anomaly score"

### Used for
- Removing outliers from datasets
- Intrusion detection
- Fraud
- Model Competence
    - After putting a model into production, data that is being predicted can become statistcally different than the training data.
    - Train an anomaly detector at the same time as the model
    - The data you are predicting doesn't match your training data (high anomaly score)
- Benford's Law
    - In real-life numeric sites the small digits occur disproportionately often as leading significant digits
- Univariate approach (using normal distribution)
- Multivariate matters
- Random splits
    - Grow a random decision tree until each instance from a sample is in its own leaf
    - It will be hard to isolate each one
    - At the end you get the average depth of each leaf (harder from easier)
    - **Isolation Forest Scoring**

## 1-Class classifier
- Get your positive class
- Use anomaly detection to check the ones different from the positive class

## Association discovery
- Unsupervised learning technique
- Finds "significant" correlations/associations/relations
- Express them as "if then" rules 

### Use cases
- Data discovery
- Market basket

### What is interesting?
- In-frequent patterns can be strong, but are they interesting?
- Frequent patterns can be strong, but are they interesting?

### Association Metrics
- Coverage
    - Percentage of instances which match antecedent "A"
        - How much of the trainig data is covered by the antecedent
- Support
    - Percentage of instancecs which match antencendet "A" and consequent "C"
- Confidence
- Lift
    - Ratio of observed support to support if A and C were statistically independent
        - Support / (p(A) * p(C)) == Confidence / p(C)
    - Problem: if p(C) is small then... lift may be large
    - < 1 = negative correlation
    - > 1 = positive correlation
    - = 1 = no corrlation
- Leverage

## Topic Models
- Learns only from text fields
- Finds hidden topics that model the text

### Intuition
- Written documents have meaning
- The topic can be thought of as increasing the probability of certain words
- Each text field in a row is concatenated into a document
- The documents are analyzed to generate "k"related topics
- Each topic is represented by a distribution of the probabilities

### Topic Distribution
- Any given document is likely a mixture of the modeled topics
- This can be represented as a distribution of topic probabilities

### Clustering
You can use the topic distribution to create new features for each row, with their probability for each topic and then generate the clusters

### Why to use TM?
- As a preprocessor for other techniques
    - Building better models
- Bootstrapping categories for classification
- Recommendation
- Discovery in large, heterogeneous text datasets

### TM Tips
- Setting k
    - Much like k=means, the best value is data specific
- Tunning the model
    - Remove common, useless terms
    - Set term limit higher

## Text analysis
- Stem words > tokens
- Remove tokens that occur too often
- Remove tokens that do not occur often enough
- Count the occurrences of remaining words
- Transform the remainig words in a vector, counting each word

## TA vs TM
|TA|TM|
|---|---|
|Creates thousands of hidden token counts|Creates tens of topics that model the text|
|Token counts are independently uninsteresting|Topics are independently interesing|
|No semantic importance|...|

## Basic Transformation
### Obstacles
- Data structure (data transformation)
    - Scattered across systems
    - Wrong shape
    - Unalbelled data
- Data value (feature engineering)
    - Format: spelling, units
    - Missing values
    - Non-optimal correlation
    - Non-existant correlation
- Data significance (feature selection)
    - Unwanted: PII, non-preferred
    - Expensive to collect
    - Isidious: leakage, obviously correlated

### Process
- Define a clear idea of the goal
    - Sometimes this come later...
    - Understand what ML tasks will achieve the goal
- Transform the data
- Feature engineering
    - Transform the data you have into the data you actually need
- Evaluate
    - Try it on a small scale
    - Accept that you might have to start over
- But when it works, automate!!!

### ML Ready Data
- Tabular data
    - Each row is one instance

### Data labelling
- Data is often not labelled
    - Create labels with a transformation

### Time Windows
Create new features using values from different time periods

### Updates
Need a current view of the data, but new data only come in batches of change

## Stream batch

## Feature Engineering
Applying domain knowledge of the data to create new features that allow ML algorithms to work better, or to work at all
- This is really important - more than algorithm selection
- ML algorithms have no deeper understanding of data
- **The magic is the ability to find patterns quickly and efficiently**
- ML algorithms only know what you tell/show it with data
- Intuition can be risky

### Feature selection
- Leakage
    - Stock close predicts stock open
    - Sales pipeline where steps n-1 has no other outcome than step n

### Evaluate & Automate

## API
- Workflow automation - reduce drudgery
- Abstraction - reuse code
- Composability - powerful combinations of APIs
- Integration
- Automate deployment
- Repeatable results

## Important infomartion about your dataset and model
### Show statistics for each field on your dataset
- Count
- Missing
- Histogram
    - How you do this for text fields?

### Show your model evaluation
- Accuracy
- Precision
- Recall
- F-measure
- Phi-coefficient

### Anomaly check
- Check for anomaly on the data before training
- Check the anomaly score of the data before predicting
