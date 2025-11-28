import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, accuracy_score
import joblib


data = pd.read_csv("Dataset.csv")

# Ensure realistic limits (since incense max = 125)
data = data[data['MQ2'] <= 200]

X = data[['MQ2', 'Temperature', 'Humidity']]
y = data['Fire_Alarm'].apply(lambda x: 1 if x == 1 else 0)  


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
rf_model = RandomForestClassifier(
    n_estimators=80,       
    max_depth=5,           
    min_samples_split=10,  
    min_samples_leaf=5,    
    random_state=42
)
rf_model.fit(X_train, y_train)
print("\n Dataset shape:", data.shape)
print("\n🎯 Random Forest Classification Report:")

y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))

iso_model = IsolationForest(contamination=0.1, random_state=42)
iso_model.fit(X)


joblib.dump(rf_model, "smoke_classifier.pkl")
joblib.dump(iso_model, "smoke_anomaly.pkl")

print("\n💾 Models saved → smoke_classifier.pkl, smoke_anomaly.pkl")
