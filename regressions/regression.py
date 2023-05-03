import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def load_data(filename):
    data = []
    label = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        reader.__next__()

        for line in reader:
            data.append(list(map(lambda x: float(x), line[:-1])))
            label.append(float(line[-1]))
    data = np.array(data)
    label = np.array(label)
    return (data, label)

x, y = load_data('./final_data.csv')


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

def rmse(predict, true):
    result = np.sqrt(np.mean((predict - true) ** 2))
    return result

def normal_rmse(predict, true):
    normalizer = np.max(true) - np.min(true)
    result = rmse(predict, true)
    result /= normalizer
    return result

model = RandomForestRegressor()
model.fit(x_train, y_train)
print('random forest')
print(rmse(model.predict(x_test), y_test))
print(normal_rmse(model.predict(x_test), y_test))
print(model.score(x_test, y_test))

def graph_with_model(model, filename, title):
    x_real, y_real = load_data(filename)

    y_pred = model.predict(x_real)

    plt.plot(y_pred, color='red', label='Ground Truth')
    plt.plot(y_real, color='blue', label='Prediction')
    plt.legend(loc='upper right')
    plt.xlabel('Months Since Release')
    plt.ylabel('Number of Active Users')
    plt.title(title)
    plt.show()

graph_with_model(model, './Intel_HD_Graphics_4600.csv', 'Intel HD Graphics 4600')
graph_with_model(model, './AMD_graphing_data.csv', 'AMD Radeon RX 500')
graph_with_model(model, './Intel_graphing_data.csv', 'Intel HD Graphics 3000')