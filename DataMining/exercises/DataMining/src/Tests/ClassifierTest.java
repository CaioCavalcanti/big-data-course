package Tests;

import Framework.J48Classifier;
import Framework.RandomForestClassifier;

public class ClassifierTest {

	public static void main(String[] args) {
		String input = "C:\\Program Files\\Weka-3-8\\data\\vote.arff";
		String j48output = "C:\\Users\\1511 IRON\\Google Drive\\UP - Pós\\Data Mining\\vote_j48.model";
		String randomForestoutput = "C:\\Users\\1511 IRON\\Google Drive\\UP - Pós\\Data Mining\\vote_randomForest.model";

		try {
			J48Classifier j48cls = new J48Classifier(input, j48output);
			j48cls.Build();

			Thread t1 = new Thread(new Runnable() {
				public void run() {
					try {
						j48cls.Evaluate();
					} catch (Exception e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			});

			t1.start();

			RandomForestClassifier randomForestCls = new RandomForestClassifier(input, randomForestoutput);
			randomForestCls.Build();

			Thread t2 = new Thread(new Runnable() {
				public void run() {
					try {
						randomForestCls.Evaluate();
					} catch (Exception e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			});

			t2.start();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
