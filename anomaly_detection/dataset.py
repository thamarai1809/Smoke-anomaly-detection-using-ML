import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Generate normal clean air readings
clean_air = pd.DataFrame({
    'MQ2': np.random.uniform(30, 60, 100),
    'Temperature': np.random.uniform(32, 34, 100),
    'Humidity': np.random.uniform(55, 65, 100),
    'Fire_Alarm': 0  # 0 = Normal
})

# Generate incense smoke readings (normal)
incense = pd.DataFrame({
    'MQ2': np.random.uniform(65, 125, 120),
    'Temperature': np.random.uniform(33, 36, 120),
    'Humidity': np.random.uniform(58, 70, 120),
    'Fire_Alarm': 1  # 1 = Smoke detected
})

# Generate few anomaly readings (rare, heavy fumes or unusual)
anomalies = pd.DataFrame({
    'MQ2': np.random.uniform(130, 180, 20),
    'Temperature': np.random.uniform(35, 38, 20),
    'Humidity': np.random.uniform(60, 80, 20),
    'Fire_Alarm': 2  # 2 = Anomaly
})

# Combine everything
data = pd.concat([clean_air, incense, anomalies], ignore_index=True)
data = data.sample(frac=1).reset_index(drop=True)  # shuffle

# Save dataset
data.to_csv("Arduino_MQ2_DHT11_SmokeDataset.csv", index=False)

print("✅ Dataset generated and saved as 'Arduino_MQ2_DHT11_SmokeDataset.csv'")
print(data.head(10))
