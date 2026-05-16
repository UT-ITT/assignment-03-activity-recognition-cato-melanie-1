# this program recognizes activities
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.preprocessing import scale, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
import glob

#load dataset
def load_data(dataset_path):
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


recordings = load_data("data")


#divide into 2s windows
def create_windows(recording):
    windows = []

    for start in range(0, len(recording) - 200, 200):
        window = recording.iloc[start:start + 200]
        windows.append(window)
    
    return windows


all_windows = []

for recording in recordings:
    windows = create_windows(recording)
    all_windows.extend(windows)


#mean and standard deviation per window for each sensor value
def extract_features(window):
    features = {}

    #Acc x
    features["mean_acc_x"] = window["acc_x"].mean()
    features["std_acc_x"] = window["acc_x"].std()

    #Acc y
    features["mean_acc_y"] = window["acc_y"].mean()
    features["std_acc_y"] = window["acc_y"].std()

    #Acc z
    features["mean_acc_z"] = window["acc_z"].mean()
    features["std_acc_z"] = window["acc_z"].std()

    #Gyro x
    features["mean_gyro_x"] = window["gyro_x"].mean()
    features["std_gyro_x"] = window["gyro_x"].std()

    #Gyro y
    features["mean_gyro_y"] = window["gyro_y"].mean()
    features["std_gyro_y"] = window["gyro_y"].std()

    #Gyro z
    features["mean_gyro_z"] = window["gyro_z"].mean()
    features["std_gyro_z"] = window["gyro_z"].std()

    features["activity"] = window["activity"].iloc[0]

    return features


all_features = []

for window in all_windows:
    feature = extract_features(window)
    all_features.append(feature)


#ML dataset
features_df = pd.DataFrame(all_features)

#split into training and test dataset
X = features_df.drop("activity", axis=1)
y = features_df["activity"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#scale
scaler = MinMaxScaler() #StandardScaler
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#print(X_train_scaled.shape)
#print(X_test_scaled.shape)

#classification using SVM
classifier = svm.SVC(kernel='poly') #rbf
classifier.fit(X_train_scaled, y_train)

zz = classifier.predict(X_test_scaled)


print(f"accuracy: {accuracy_score(y_test, zz)}")
print(classification_report(y_test, zz))

