# Smart Health Monitoring System using Python and ESP32 Simulation

A simulation-based smart health monitoring project that reads **heart rate**, **oxygen level**, and **temperature** using ESP32 with virtual sensor inputs. The project collects sensor data, saves it into a CSV file, and uses Python machine learning models to classify the patient status as normal or abnormal.

## Project Overview

This project is designed as a **health monitoring prototype** for portfolio and internship use.  
It uses:
- Potentiometer 1 for simulated heart rate input
- Potentiometer 2 for simulated oxygen input
- NTC thermistor for temperature
- OLED display for live values
- Buzzer for alert generation

The collected data is stored in CSV format and can be used to train and compare multiple machine learning models.

## Features

- Real-time simulated health sensor monitoring
- OLED display for live readings
- Buzzer alert for abnormal readings
- CSV data collection for machine learning
- Multiple ML model testing and comparison
- Easy to extend into a full IoT + ML project

## Hardware / Components Used

### Simulation Hardware
- ESP32
- 2 Potentiometers
- NTC Thermistor
- OLED Display (SSD1306)
- Buzzer

### Software Tools
- Wokwi / ESP32 Simulator
- Arduino IDE / PlatformIO
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit

## Project Workflow

1. Simulate sensor readings in Wokwi.
2. ESP32 reads heart rate, oxygen, and temperature values.
3. Data is printed through Serial Monitor.
4. Python script collects the serial data and saves it into `data.csv`.
5. Machine learning models are trained on the CSV file.
6. Best model is selected and used for prediction.
7. Optional Streamlit dashboard shows results.

## File Structure

```bash
Smart Health Monitoring/
│
├── src/
│   └── main.cpp
├── collect_data.py
├── json_to_excel.py
├── diagram.json
├── wokwi.toml
├── data.csv
└── README.md
```

## How to Run

### 1. Open the simulation
- Load the project in Wokwi or your ESP32 simulator.
- Make sure the circuit is connected properly.

### 2. Upload / run the ESP32 code
- Use `src/main.cpp` for the simulation logic.
- Check readings in the Serial Monitor.

### 3. Collect the dataset
- Run `collect_data.py` to capture serial data.
- Save the output into `data.csv`.

### 4. Train ML models
- Use Python to load the CSV.
- Try multiple models such as:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - SVM
  - KNN
  - Naive Bayes

### 5. Build prediction app
- Use Streamlit to create a simple interface for model selection and prediction.

## Dataset Format

The CSV file contains readings like:

- `temperature`
- `pot1`
- `pot2`

Example:

```csv
temperature,pot1,pot2,label
25.5,620,304,normal
33.5,1185,789,warning
18.9,4095,3731,critical
```

## Model Ideas

You can compare multiple models and allow the user to select one:
- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- KNN
- Naive Bayes
- Gradient Boosting

## Use Case

This project can be presented as a:
- Smart health monitoring prototype
- Simulated patient monitoring system
- ML-based abnormal condition detector
- Internship portfolio project

## Important Note

This project uses **simulated sensor data**, not medical-grade sensor data. It is built for learning, prototyping, and portfolio demonstration.

## Future Improvements

- Add real sensors later
- Add live dashboard using Streamlit
- Add model comparison chart
- Add confusion matrix and performance metrics
- Deploy the app online
- Connect real IoT hardware

## Author

Created as a Python + ESP32 + ML health monitoring project for learning and portfolio building.
