# sentiment_analisis.py

import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

# Path untuk model dan file CSV
h5_model_path = './model_save/sentiment_models/indobert_model_tf_category.h5'  # Ganti dengan path yang sesuai untuk model IndoBERT Anda
csv_file_path = '../../hasil_scrapping_antara/automasi_antara.csv'  # Ganti dengan path yang sesuai untuk file CSV Anda
data = pd.read_csv(csv_file_path)
print(data.head())

# Memuat tokenizer
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p2")

# Inisialisasi model
model = TFBertForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p2", num_labels=3)

# Memuat bobot model dari file H5
model.load_weights(h5_model_path)

# Membaca file CSV
df = pd.read_csv(csv_file_path)

# Preprocessing teks pada kolom 'content'
def preprocess(texts, tokenizer, max_len=128):
    encodings = tokenizer.batch_encode_plus(
        texts.tolist(),
        truncation=True,
        padding='max_length',
        max_length=max_len,
        return_tensors='tf'
    )
    return encodings

encodings = preprocess(df['content'], tokenizer)

# Melakukan prediksi
predictions = model(encodings['input_ids'], attention_mask=encodings['attention_mask'])
predicted_labels = np.argmax(predictions.logits, axis=1)

# Mengonversi hasil prediksi menjadi label
sentiment_labels = ['netral', 'negatif', 'positif']
df['sentimen'] = [sentiment_labels[label] for label in predicted_labels]

# Menyimpan file CSV yang telah diperbarui
output_file_path = './hasil_predik/automasi_antara_with_sentiment.csv'
df.to_csv(output_file_path, index=False)

print("Prediksi sentimen telah selesai dan disimpan ke", output_file_path)
