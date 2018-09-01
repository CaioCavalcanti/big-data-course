package Framework;

import java.util.Random;

import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.core.converters.ConverterUtils.DataSource;

public class RandomForestClassifier {
	private String _sourceInput;
	private String _modelOutput;
	private Instances _data;

	public RandomForestClassifier(String sourceInput, String modelOutput) throws Exception {
		super();
		this._sourceInput = sourceInput;
		this._modelOutput = modelOutput;

		// Open data source
		// Using vote dataset from weka examples
		DataSource source = new DataSource(this._sourceInput);

		// Convert source to instances
		// Instance is the object type that weka uses on its algorithms
		_data = source.getDataSet();

		// Indicate the class
		// in this case is the last column
		_data.setClassIndex(_data.numAttributes() - 1);
	}

	public void Build() throws Exception {
		// Create new classifier using Random Forest
		RandomForest randomForest = new RandomForest();

		// Set the options
		String strOptions = "-P 100 -print -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1";
		String[] options = strOptions.split(" ");
		randomForest.setOptions(options);

		// Build classifier using the data
		randomForest.buildClassifier(_data);

		// Save model
		weka.core.SerializationHelper.write(this._modelOutput, randomForest);

		// Print model
		System.out.println(randomForest.toString());

		// TODO: parse to json and store on a db (NoSQL for better performance) for
		// explanation
	}

	public void Evaluate() throws Exception {
		// Creates new classifier, loading the model generated on build
		RandomForest randomForest = (RandomForest) SerializationHelper.read(this._modelOutput);

		// Create object for evaluation
		Evaluation eval = new Evaluation(_data);

		// Executes cross validation
		// requires random number and num of folds
		eval.crossValidateModel(randomForest, _data, 10, new Random());

		// Shows model accuracy
		System.out.println(eval.toSummaryString());
		System.out.println(eval.toClassDetailsString());
		System.out.println(eval.toMatrixString());
	}

}
