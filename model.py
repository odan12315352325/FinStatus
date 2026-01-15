import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Model
from keras.layers import Input, Dense, Dropout, BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.regularizers import l2
from keras.utils import plot_model
import matplotlib.pyplot as plt

file_path = './dataSET.csv'
data = pd.read_csv(file_path, delimiter=';')

X = data.iloc[:, :35].values
y_regression = data.iloc[:, 35:46].values
y_classification = data.iloc[:, 46].values

#Масштабирование входных данных#
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Разделение данных на обучающую и тестовую выборки#
X_train, X_test, y_train_reg, y_test_reg, y_train_cls, y_test_cls = train_test_split(
    X_scaled, y_regression, y_classification, test_size=0.2, random_state=42
)

#Преобразование меток классификации в формат подходящий для Keras#
y_train_cls = y_train_cls.reshape(-1, 1)
y_test_cls = y_test_cls.reshape(-1, 1)

input_layer = Input(shape=(35,))

hidden_layer = Dense(128, activation='relu', kernel_regularizer=l2(0.001))(input_layer)
hidden_layer = BatchNormalization()(hidden_layer)
hidden_layer = Dropout(0.3)(hidden_layer)

model = Model(inputs=input_layer, outputs=[output_regression, output_classification])

model.compile(optimizer=Adam(learning_rate=0.001),
            loss={'regression_output': 'mse', 'classification_output': 'binary_crossentropy'},
            metrics={'classification_output': 'accuracy'})

#Ранняя остановка и снижение скорости обучения на плато#
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)

history = model.fit(X_train, {'regression_output': y_train_reg, 'classification_output': y_train_cls},
                    validation_data=(X_test, {'regression_output': y_test_reg, 'classification_output': y_test_cls}),
                    epochs=100, batch_size=32, callbacks=[early_stopping, reduce_lr])

model.save('financial_model.h5')