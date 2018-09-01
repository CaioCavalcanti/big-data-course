package Framework;

import java.util.Random;

import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.trees.J48;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.core.converters.ConverterUtils.DataSource;

public class J48Classifier {
	private String _sourceInput;
	private String _modelOutput;
	private Instances _data;

	public J48Classifier(String sourceInput, String modelOutput) throws Exception {
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
		// Create new classifier
		// using J48 (C4.5)
		J48 j48 = new J48();

		// Set the options
		j48.setMinNumObj(2); // Min objects generated
		j48.setUnpruned(true); // Disable unpruned, to get all nodes on the tree

		// Build classifier using the data
		j48.buildClassifier(_data);

		// Save model
		weka.core.SerializationHelper.write(this._modelOutput, j48);

		// Print model
		System.out.println(j48.toString());

		// TODO: parse to json and store on a db (NoSQL for better performance) for
		// explanation
	}

	public void Evaluate() throws Exception {
		// Creates new classifier, loading the model generated on build
		J48 j48 = (J48) SerializationHelper.read(this._modelOutput);

		// Create object for evaluation
		Evaluation eval = new Evaluation(_data);

		// Executes cross validation
		// requires random number and num of folds
		eval.crossValidateModel(j48, _data, 10, new Random());

		// Shows model accuracy
		System.out.println(eval.toSummaryString());
		System.out.println(eval.toClassDetailsString());
		System.out.println(eval.toMatrixString());
	}
}
