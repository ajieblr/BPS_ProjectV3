import pandas as pd
import numpy as np
import re
import os
import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Bidirectional, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout
from sklearn.metrics import classification_report, confusion_matrix
from nltk.corpus import wordnet

import nltk
nltk.download('wordnet')

import random

# Load data
labeled_data = pd.read_csv('../data/training_data.csv')

# Ensure all entries in 'content' are strings
labeled_data['content'] = labeled_data['content'].astype(str)

# Preprocess text
def preprocess(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

labeled_data['content'] = labeled_data['content'].apply(preprocess)

# Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(labeled_data['content'].values)
X = tokenizer.texts_to_sequences(labeled_data['content'].values)
X = pad_sequences(X, maxlen=150)  # Adjust sequence length
Y = pd.get_dummies(labeled_data['label']).values

# Split data
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

# Data augmentation functions
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if wordnet.synsets(word)]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = wordnet.synsets(random_word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break
    return new_words

def random_deletion(words, p):
    if len(words) == 1:
        return words
    return [word for word in words if random.uniform(0, 1) > p]

def augment_text(text):
    words = text.split()
    augmented_texts = [
        ' '.join(synonym_replacement(words, n=1)),
        ' '.join(random_deletion(words, p=0.1))
    ]
    return augmented_texts

# Apply data augmentation
augmented_texts = []
augmented_labels = []

for i, text in enumerate(labeled_data['content']):
    augmented_texts.extend(augment_text(text))
    augmented_labels.extend([labeled_data['label'].values[i]] * len(augment_text(text)))

# Prepare augmented data
augmented_data = pd.DataFrame({
    'content': augmented_texts,
    'label': augmented_labels
})

# Tokenize and pad augmented data
augmented_sequences = tokenizer.texts_to_sequences(augmented_data['content'].values)
augmented_sequences = pad_sequences(augmented_sequences, maxlen=150)

X_train_augmented = np.concatenate((X_train, augmented_sequences), axis=0)
Y_train_augmented = np.concatenate((Y_train, pd.get_dummies(augmented_data['label']).values), axis=0)

# Build model
def build_model(vocab_size, input_length, num_classes):
    inputs = Input(shape=(input_length,))
    x = Embedding(input_dim=vocab_size, output_dim=128)(inputs)
    x = Bidirectional(LSTM(128, return_sequences=True))(x)
    x = Dropout(0.5)(x)
    x = Bidirectional(LSTM(128))(x)
    x = Dropout(0.5)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

model = build_model(len(tokenizer.word_index) + 1, 150, Y.shape[1])
model.summary()

# Train model
history = model.fit(X_train_augmented, Y_train_augmented, epochs=10, batch_size=64,
                    validation_data=(X_val, Y_val))

# Save model
model.save('model_save/model_category/news_classifyAug_model.h5')
