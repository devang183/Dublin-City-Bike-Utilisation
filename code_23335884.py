# -*- coding: utf-8 -*-
"""code-23335884.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DlknnMeaBSqPnQEqt7Tw-TFPX2BgQX5X
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('\combined_cleaned_data.csv', parse_dates=['TIME'])


pandemic_start = pd.Timestamp('2020-03-01')
pandemic_end = pd.Timestamp('2021-03-01')

def categorize_period(row):
    if row < pandemic_start:
        return 'Pre-Pandemic'
    elif pandemic_start <= row <= pandemic_end:
        return 'Pandemic'
    else:
        return 'Post-Pandemic'

df['Period'] = df['TIME'].apply(categorize_period)

bike_usage_by_period = df.groupby('Period')['bikes taken'].sum()

total_bikes_used=bike_usage_by_period.sum()
plt.figure(figsize=(8, 8))
bike_usage_by_period.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Bike Usage Distribution Among Different Pandemic Phases')
plt.ylabel('')

legend_labels = [f'{phase}: {count}' for phase, count in zip(bike_usage_by_period.index, bike_usage_by_period)]
plt.legend(legend_labels + [f'Total: {total_bikes_used}'], title='Pandemic Phase', loc='upper right')

plt.show()

df.head()

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('\combined_cleaned_data.csv', parse_dates=['TIME'])
df['TIME'] = pd.to_datetime(df['TIME'])
df['TIME']=df['TIME'].dt.strftime('%Y-%m-%d')
df['TIME'] = pd.to_datetime(df['TIME'])
df.set_index('TIME',inplace=True)
altered_df=df['bikes taken'].resample('3D').mean()

altered_df.head()

altered_df.shape

altered_df.to_csv('altered_data.csv',index=True)

plt.figure(figsize=(30, 15))
plt.plot(altered_df.index, altered_df.values, marker='o', linestyle='-')
plt.title('Bike  (3D Mean)')
plt.xlabel('Time')
plt.ylabel('Average Available Bikes')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

!pip install tqdm

import pandas as pd
from tqdm import tqdm

file_path = 'altered_data.csv'
df = pd.read_csv(file_path, encoding='ascii')

df_head = df.head()
print(df_head)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
df['bikes taken'].plot(kind='hist', bins=30, alpha=0.7)
plt.title('Distribution of Average Bikes Taken per 3 Days')
plt.xlabel('Average Bikes Taken')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

!pip install scikit-learn

df['TIME']=pd.to_datetime(df['TIME'])
df.sort_values('TIME',inplace=True)

pandemic_start = pd.to_datetime('2020-01-01')
df_pandemic = df[df['TIME'] >= pandemic_start]

df_pandemic.isnull().sum()

df_pandemic.dropna(subset=['bikes taken'], inplace=True)

df_pandemic.isnull().sum()

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from tqdm import tqdm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import AdaBoostRegressor

X = df_pandemic[['TIME']].apply(lambda x: x.map(datetime.toordinal)) # Convert dates to ordinal
y = df_pandemic['bikes taken']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    'K-Nearest Neighbors': KNeighborsRegressor(),
    'Ridge Regression': Ridge(),
    'AdaBoost': AdaBoostRegressor()
}

predictions = {}

knn_model = models['K-Nearest Neighbors']
knn_model.fit(X_train_scaled, y_train)
predictions['K-Nearest Neighbors'] = knn_model.predict(X_test_scaled)

ridge_model = models['Ridge Regression']
ridge_model.fit(X_train_scaled, y_train)
predictions['Ridge Regression'] = ridge_model.predict(X_test_scaled)

adaboost_model = models['AdaBoost']
adaboost_model.fit(X_train_scaled, y_train)
predictions['AdaBoost'] = adaboost_model.predict(X_test_scaled)

mse_scores = {
    'K-Nearest Neighbors': mean_squared_error(y_test, predictions['K-Nearest Neighbors']),
    'Ridge Regression': mean_squared_error(y_test, predictions['Ridge Regression']),
    'AdaBoost': mean_squared_error(y_test, predictions['AdaBoost'])
}

print(mse_scores)

import matplotlib.pyplot as plt

model_names = list(mse_scores.keys())
mse_values = list(mse_scores.values())

plt.figure(figsize=(10, 5))
plt.bar(model_names, mse_values, color='skyblue')
plt.title('Mean Squared Error of Different Models')
plt.ylabel('Mean Squared Error')
plt.xlabel('Model')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

!pip install numpy

from datetime import datetime
import numpy as np

X_test_dates = scaler.inverse_transform(X_test_scaled)

X_test_dates = [datetime.fromordinal(int(date)) for date in X_test_dates.flatten()]

sorted_indices = np.argsort(X_test_dates)
X_test_dates_sorted = np.array(X_test_dates)[sorted_indices]

plt.figure(figsize=(14, 7))
plt.scatter(X_test_dates_sorted, y_test.iloc[sorted_indices], color='black', label='True Values')

for name, y_pred in predictions.items():
    plt.plot(X_test_dates_sorted, y_pred[sorted_indices], label=name)

plt.title('Predictions of Different Models vs True Values')
plt.xlabel('Date')
plt.ylabel('Bikes Taken')
plt.legend()
plt.tight_layout()
plt.show()

pandemic_data = altered_df.loc[altered_df.index >= '2020-03-01']

pandemic_data['days_since_start'] = (pandemic_data.index - pandemic_data.index[0]).days

X_pandemic = pandemic_data['days_since_start'].values.reshape(-1, 1)
y_pandemic = pandemic_data['bikes taken'].values

knn_predictions_pandemic = knn_model.predict(X_pandemic)
ridge_predictions_pandemic = ridge_model.predict(X_pandemic)
ada_predictions_pandemic = ada_model.predict(X_pandemic)

plt.figure(figsize=(15, 7))
plt.plot(pandemic_data.index, y_pandemic, label='Real Data', color='blue', linestyle='-')
plt.plot(pandemic_data.index, knn_predictions_pandemic, label='KNN Predictions', color='red', linestyle='-')
plt.plot(pandemic_data.index, ridge_predictions_pandemic, label='Ridge Predictions', color='green', linestyle='-')
plt.plot(pandemic_data.index, ada_predictions_pandemic, label='AdaBoost Predictions', color='purple', linestyle='-')
plt.title('Pandemic Period Real vs Predicted Bikes Taken')
plt.xlabel('Date')
plt.ylabel('Bikes Taken')
plt.legend()
plt.show()
