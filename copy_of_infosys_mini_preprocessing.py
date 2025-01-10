# -*- coding: utf-8 -*-
"""Copy of infosys mini preprocessing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RdIyaKA-sw7zO-J34aejs-vIpb4Vh3ZP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


file_path = '/content/Energy_consumption_with_HomeID.csv'
data = pd.read_csv(file_path)


print("First 5 Rows:")
print(data.head())

print("\nData Summary:")
print(data.info())

print("\nStatistics:")
print(data.describe())


print("\nMissing Values Before Replacement:")
print(data.isnull().sum())

# Replace missing numerical values with the mean
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
for col in numerical_columns:
    data[col].fillna(data[col].mean(), inplace=True)

# Replace missing categorical values with the mode
categorical_columns = data.select_dtypes(include=['object']).columns
for col in categorical_columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

print("\nMissing Values After Replacement:")
print(data.isnull().sum())


for col in numerical_columns:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=data[col])
    plt.title(f"Boxplot of {col}")
    plt.show()


for col in numerical_columns:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data[col] = np.where(data[col] < lower_bound, data[col].median(), data[col])
    data[col] = np.where(data[col] > upper_bound, data[col].median(), data[col])




sns.pairplot(data, diag_kind="kde", corner=True)
plt.title("Pairplot of the Dataset")
plt.show()


plt.figure(figsize=(8, 4))
sns.histplot(data['EnergyConsumption'], kde=True, bins=20, color='blue')
plt.title("Distribution of Energy Consumption")
plt.show()


print("\nFinal Processed Data:")
print(data.head())

# 1. Correlation heatmap
plt.figure(figsize=(10, 6))

numerical_data = data.select_dtypes(include=['number'])
sns.heatmap(numerical_data.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '/content/Energy_consumption_with_HomeID.csv'
data = pd.read_csv(file_path)

# Data Preprocessing
# 1. Convert Timestamp to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# 2. Handle missing values
# Replace missing numerical values with mean
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
for col in numerical_columns:
    data[col].fillna(data[col].mean(), inplace=True)

# Replace missing categorical values with mode
categorical_columns = data.select_dtypes(include=['object']).columns
for col in categorical_columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

# 3. Encode categorical variables
categorical_columns = ['HVACUsage', 'LightingUsage', 'DayOfWeek', 'Holiday']
for col in categorical_columns:
    data[col] = data[col].astype('category').cat.codes

# 4. Scale numerical features
numerical_columns = ['Temperature', 'Humidity', 'SquareFootage', 'RenewableEnergy','HomeID']
data[numerical_columns] = (data[numerical_columns] - data[numerical_columns].mean()) / data[numerical_columns].std()

# 5. Drop unnecessary columns
data = data.drop(columns=['Timestamp'])

# 6. Define features and target
X = data.drop(columns=['EnergyConsumption'])
y = data['EnergyConsumption']

# 7. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
# 1. Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
# 1. Predict on test data
y_pred = model.predict(X_test)

# 2. Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

# Visualization
# 1. Feature Importance
plt.figure(figsize=(10, 6))
importance = pd.Series(model.feature_importances_, index=X.columns)
importance.nlargest(10).sort_values().plot(kind='barh')
plt.title("Feature Importance")
plt.show()

# 2. Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.xlabel('Actual Energy Consumption')
plt.ylabel('Predicted Energy Consumption')
plt.title('Actual vs Predicted')
plt.show()

# Print actual vs predicted values side-by-side
actual_vs_predicted = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(actual_vs_predicted.head(10))

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Evaluate regression performance
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score

# Assuming energy levels are bucketed into categories
bins = [y.min(), y.quantile(0.33), y.quantile(0.66), y.max()]
labels = ['Low', 'Medium', 'High']
y_test_binned = pd.cut(y_test, bins=bins, labels=labels, include_lowest=True)
y_pred_binned = pd.cut(y_pred, bins=bins, labels=labels, include_lowest=True)

# Confusion matrix
conf_matrix = confusion_matrix(y_test_binned, y_pred_binned, labels=labels)

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')
plt.title('Confusion Matrix')
plt.show()

# Print accuracy score
accuracy = accuracy_score(y_test_binned, y_pred_binned)
print(f"Accuracy: {accuracy:.2f}")