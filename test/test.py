MODEL_PATH = "../lstm/lstm_stock_mashiro.pt"

import numpy as np
import matplotlib.pyplot as plt
import random
import torch
from sklearn.preprocessing import MinMaxScaler
from lstm import model

# 假设模型已经被实例化并加载了训练好的权重
model = model.LSTMModel()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

# 生成随机初始值
def generate_random_initial_values(num_values=1000):
    base_price=random.uniform(30,80)
    res=[base_price]
    for _ in range(num_values-1):
        # 随机波动范围
        
        lower_volatility = random.uniform(-10, -1)  # 最小波动
        upper_volatility = random.uniform(1, 10)    # 最大波动
        volatility = random.uniform(lower_volatility, upper_volatility)
        stock_price = round(base_price + volatility, 2)
        if stock_price < 60:
            stock_price = 60+random.uniform(1,10)
        elif stock_price > 120:
            stock_price = 120-random.uniform(1,10)  # 保证在60-120之间
        base_price=stock_price
        res.append(stock_price)
    return torch.tensor(res)

    # return np.random.rand(num_values) * (120 - 60) + 60

# 生成初始值并转换为 NumPy 数组
random_initial_values = generate_random_initial_values()
initial_tensor = random_initial_values.reshape(-1, 1)  # 转换为列向量

# 创建 MinMaxScaler 实例并拟合初始值
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_initial_tensor = scaler.fit_transform(initial_tensor)

# 准备数据以适应 LSTM 输入格式
initial_tensor_lstm = torch.tensor(scaled_initial_tensor, dtype=torch.float32).view(1, -1, 1)

# 用于存储预测结果
predictions = []

# 进行 1000 次预测
with torch.no_grad():
    for _ in range(128):
        # 进行一次预测
        prediction = model(initial_tensor_lstm)
        predictions.append(prediction.item())
        
        # 更新输入张量以包含最新的预测值
        initial_tensor_lstm = torch.cat((initial_tensor_lstm[:, 1:, :], prediction.view(1, 1, 1)), dim=1)

# 对预测结果进行反缩放
predicted_values_unscaled = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# 绘制股价预测图
plt.figure(figsize=(12, 6))
plt.plot(initial_tensor.numpy(), label='Initial Stock Prices', color='orange')  # 原始随机初始值
plt.plot(np.arange(len(initial_tensor), len(initial_tensor) + len(predicted_values_unscaled)), predicted_values_unscaled, label='Stock Price Prediction', color='blue')  # 预测数据
plt.title('Stock Price Prediction Over 128 Steps')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.legend()
plt.grid()

# 保存图像为文件
plt.savefig('stock_price_prediction.png')  # 你可以更改文件名
plt.close()  # 关闭图形以释放内存

# 输出结果
print("随机初始值:", initial_tensor.flatten())  # 直接打印 NumPy 数组
print("缩放后的初始值:", scaled_initial_tensor.flatten())
print("前 10 个预测结果（反缩放后）:", predicted_values_unscaled[:100].flatten())