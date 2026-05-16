import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
import glob

class ActivityRecognizer:

    def __init__(self):
        #classification using SVM
        self.classifier = svm.SVC(kernel='rbf')

        #scale
        self.scaler = StandardScaler()


    #load dataset
    def load_data(self, dataset_path):
        recordings = []

        activities = ["jumpingjacks", "running", "rowing", "lifting"]
        
        for activity in activities:
            activity_path = os.path.join(dataset_path, activity)

            csv_files = glob.glob(os.path.join(activity_path, "*.csv"))

            for file in csv_files:
                df = pd.read_csv(file)
                df["activity"] = activity

                recordings.append(df)

        return recordings


    #divide into 2s windows
    def create_windows(self, recording):
        windows = []

        for start in range(0, len(recording) - 200 + 1, 100):
            window = recording.iloc[start:start + 200]
            windows.append(window)
        
        return windows


    #features
    def extract_features(self, window):
        features = {}

        sensors = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]

        for sensor in sensors:
            features[f"mean_{sensor}"] = window[sensor].mean()
            features[f"std_{sensor}"] = window[sensor].std()
            features[f"min_{sensor}"] = window[sensor].min()
            features[f"max_{sensor}"] = window[sensor].max()

        if "activity" in window.columns:
            features["activity"] = window["activity"].iloc[0]

        return features
    

    def train(self):
        recordings = self.load_data("dataset")

        all_features = []

        for recording in recordings:
            windows = self.create_windows(recording)

            for window in windows:
                feature = self.extract_features(window)
                all_features.append(feature)


        #ML dataset
        features_df = pd.DataFrame(all_features)

        #split into training and test dataset
        X = features_df.drop("activity", axis=1)
        y = features_df["activity"]

        #split        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        #scale
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        #classification using SVM
        self.classifier.fit(X_train_scaled, y_train)


        predictions = self.classifier.predict(X_test_scaled)


        print(accuracy_score(y_test, predictions))
        print(classification_report(y_test, predictions))


    def predict(self, window):
        feature = self.extract_features(window)

        X = pd.DataFrame([feature])

        X_scaled = self.scaler.transform(X)

        prediction = self.classifier.predict(X_scaled)[0]

        return prediction
