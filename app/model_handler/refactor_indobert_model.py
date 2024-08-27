import os
import pandas as pd
import numpy as np
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class SentimentAnalysis:
    def __init__(self, model_path, csv_file_path):
        self.model_path = model_path
        self.csv_file_path = csv_file_path
        self.tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
        self.model = TFBertForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p2", num_labels=3)
        self.model.load_weights(self.model_path)
        self.sentiment_labels = ['netral', 'negatif', 'positif']

    def preprocess(self, texts, max_len=128):
        encodings = self.tokenizer.batch_encode_plus(
            texts.tolist(),
            truncation=True,
            padding='max_length',
            max_length=max_len,
            return_tensors='tf'
        )
        return encodings

    def predict_sentiments(self):
        df = pd.read_csv(self.csv_file_path)
        encodings = self.preprocess(df['content'])
        predictions = self.model(encodings['input_ids'], attention_mask=encodings['attention_mask'])
        predicted_labels = np.argmax(predictions.logits, axis=1)
        df['sentimen'] = [self.sentiment_labels[label] for label in predicted_labels]
        return df

    def save_predictions(self, output_file_path):
        df = self.predict_sentiments()
        df.to_csv(output_file_path, index=False)
        print("Prediksi sentimen telah selesai dan disimpan ke", output_file_path)

# Usage example
# if __name__ == "__main__":
    # model_path = './model_save/sentiment_models/indobert_model_tf_category.h5'
    # csv_file_path = '../../hasil_scrapping_antara/automasi_antara.csv'
    # output_file_path = './hasil_predik/automasi_antara_with_sentiment.csv'

    # sentiment_analysis = SentimentAnalysis(model_path, csv_file_path)
    # sentiment_analysis.save_predictions(output_file_path)
