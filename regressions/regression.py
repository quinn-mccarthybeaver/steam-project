import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split

day0 = datetime.strptime('2002-01-06', '%Y-%M-%d').date()

x = []
y = []
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
    result = np.sqrt(np.mean((predict - true) ** 2))
    result /= normalizer
    # result = np.mean((predict - true) ** 2)
    return result

model = RandomForestRegressor()
# model = ExtraTreesRegressor()
model.fit(x_train, y_train)
print('random forest')
print(rmse(model.predict(x_test), y_test))
print(normal_rmse(model.predict(x_test), y_test))
print(model.score(x_test, y_test))


x_real = []
y_real = []

x_real, y_real = load_data('./graphing_data.csv')

y_pred = model.predict(x_real)

plt.plot(y_pred, color='red', label='Ground Truth')
plt.plot(y_real, color='blue', label='Prediction')
plt.legend(loc='upper right')
plt.show()