# AI-Powered Air Quality Monitoring Dashboard

## Project objective
Build a software prototype that demonstrates:
- Problem identification
- Requirement analysis
- Network architecture
- Cloud architecture
- AI integration
- IoT architecture (simulated)
- Cybersecurity
- Prototype implementation
- System workflow
- Testing and expected outcomes

## Technology
Python, Streamlit, Pandas, NumPy, Plotly, Scikit-learn, SQLite, Joblib.

## Setup

1. Open the project folder in VS Code.
2. Open Terminal.
3. Create a virtual environment:

Windows:
python -m venv venv
venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

4. Install packages:
pip install -r requirements.txt

5. Generate synthetic IoT data:
python generate_data.py

6. Train the ML model:
python train_model.py

7. Start the dashboard:
streamlit run app.py

8. Open the local Streamlit URL shown in the terminal.

Demo login:
Username: admin
Password: admin123

## Files

generate_data.py
    Creates simulated IoT readings.

train_model.py
    Trains the Random Forest classifier and saves the model.

database.py
    Creates and reads the SQLite database.

sensor_simulator.py
    Optional simple IoT sensor simulator.

app.py
    Main Streamlit dashboard.

## Important academic note
The dataset is synthetic and the air-quality categories are project-defined for demonstration.
For a real deployment, use calibrated sensors, an approved air-quality standard,
secure cloud infrastructure and validated environmental data.
