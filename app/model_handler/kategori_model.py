import pandas as pd
import numpy as np
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from datetime import datetime as dt, timedelta
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Dropout

yesterday = dt.now() - timedelta(days=1)
start_date = yesterday
end_date = yesterday



import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


model_path = 'model_save/model_category/news_classifyAug_model.h5'
csv_path = 'hasil_predik/Predict_20240720_to_20240720.csv'
# Load the model
try:
    model = load_model(model_path, custom_objects={'Bidirectional': Bidirectional, 'LSTM': LSTM, 'Dense': Dense, 'Dropout': Dropout})
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Load the CSV file
try:
    df = pd.read_csv(csv_path)
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV file: {e}")

if 'content' not in df.columns:
    raise ValueError("'content' column not found in the CSV file")


# Prepare the tokenizer
# Note: You should use the same tokenizer used during model training
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['content'])

# Convert texts to sequences
sequences = tokenizer.texts_to_sequences(df['content'])
maxlen = 150  # Adjust maxlen as per your model's requirement
padded_sequences = pad_sequences(sequences, maxlen=maxlen)

# Make predictions
predictions = model.predict(padded_sequences)

# Assuming the model output is a probability distribution over categories
categories = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "MN", "O", "P", "Q", "RSTU", "Z1", "Z2", "Z3", "Z4", "Z5", "XX"]  # Replace with your actual categories
predicted_categories = [categories[pred.argmax()] for pred in predictions]
predicted_probabilities = [pred.max() for pred in predictions]

# Add predictions to the DataFrame
df['predicted_category'] = predicted_categories
df['predicted_probability'] = predicted_probabilities

# Save the updated DataFrame back to CSV
df.to_csv(f'Predict_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv', index=False)
