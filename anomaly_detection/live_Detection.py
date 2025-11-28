import serial
import time
import joblib
import pandas as pd



classifier = joblib.load('smoke_classifier.pkl')
anomaly_detector = joblib.load('smoke_anomaly.pkl')


feature_names = ['MQ2', 'Temperature', 'Humidity']

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
time.sleep(2)
print("✅ Connected to Arduino\nWaiting for live sensor data...\n")

try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()

            if ',' in line:
                try:
                    mq2, temp, hum = map(float, line.split(','))
                    X_live = pd.DataFrame([[mq2, temp, hum]], columns=feature_names)

                    #  Step 1: Classification (Normal / Smoke)
                    pred = classifier.predict(X_live)[0]
                    label = "Smoke" if pred == 1 else "Normal"

                    #  Step 2: Anomaly detection
                    anomaly_flag = anomaly_detector.predict(X_live)[0]
                    is_anomaly = anomaly_flag == -1

                    #  Step 3: Display results
                    if is_anomaly:
                        status = "⚠️ Anomaly Detected! 🚨 (Unusual smoke or gas)"
                    else:
                        status = "✅ Normal pattern"

                    print(f"Smoke: {mq2:.1f}, Temp: {temp:.1f}°C, Hum: {hum:.1f}% → {label} | {status}")

                    #  Step 4: Send signal back to Arduino (1 = alert, 0 = normal)
                    arduino.write(f"{1 if is_anomaly else 0}\n".encode())

                except ValueError:
                    pass

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
    arduino.close()
