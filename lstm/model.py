import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

# Create directory for saving images if it doesn't exist

# Load all CSV files and return a mapping of filename to data
def load_data_from_csv(directory):
    company_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, sep='\t')  # Adjust separator as needed
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            company_data[filename] = df[['Stock Price']]
            print(f"Loaded data from {filename}, shape: {df.shape}")  # Print info for each file
    return company_data

# Load data

# LSTM Model Definition
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=5, dropout=0.1):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Get the last output
        return out



if __name__ == "__main__":
        
    company_data = load_data_from_csv('../data/stock_logs/')
    os.makedirs('./imgs/', exist_ok=True)

    # Train and predict each company's model
    model = LSTMModel()
    for filename, data in company_data.items():
        # Normalize data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)

        # Create training and testing datasets
        train_size = int(len(scaled_data) * 0.6)
        train_data = scaled_data[:train_size]
        test_data = scaled_data[train_size:]

        # Function to create datasets
        def create_dataset(dataset, time_step=1):
            X, y = [], []
            for i in range(len(dataset) - time_step - 1):
                a = dataset[i:(i + time_step), 0]
                X.append(a)
                y.append(dataset[i + time_step, 0])
            return np.array(X), np.array(y)

        # Set time step
        time_step = 128  # Use the past 20 days to predict the next day
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, y_test = create_dataset(test_data, time_step)

        # Convert to PyTorch tensors
        X_train = torch.tensor(X_train, dtype=torch.float32)
        y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
        X_test = torch.tensor(X_test, dtype=torch.float32)
        y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

        # Reshape input data to [samples, time steps, features]
        X_train = X_train.view(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.view(X_test.shape[0], X_test.shape[1], 1)

        # Instantiate model
        

        # Define loss function and optimizer
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        num_epochs = 16
        for epoch in range(num_epochs):
            model.train()
            optimizer.zero_grad()
            outputs = model(X_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 10 == 0:
                print(f'[{filename}] Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        # Prediction
        model.eval()
        train_predict = model(X_train).detach().numpy()
        test_predict = model(X_test).detach().numpy()

        # Inverse normalization
        train_predict = scaler.inverse_transform(train_predict)
        test_predict = scaler.inverse_transform(test_predict)

        # Save plot as an image
        plt.figure(figsize=(14, 5))
        plt.plot(data.index, data['Stock Price'], label='Actual Stock Price', color='blue')
        plt.plot(data.index[time_step:len(train_predict) + time_step], train_predict, label='Training Prediction', color='orange')
        plt.plot(data.index[len(train_predict) + (time_step * 2) + 1:len(data) - 1], test_predict, label='Testing Prediction', color='green')
        plt.title(f'Stock Price Prediction for {filename}')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.savefig(f'./imgs/{filename}_prediction.png')  # Save the figure
        plt.close()  # Close the figure to free memory

    torch.save(model.state_dict(), f'lstm_stock_mashiro.pt')  # Save the model state
    print("训练完成，模型得以成功保存！")