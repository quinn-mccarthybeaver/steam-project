import csv
import numpy as np
from datetime import datetime
# from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

day0 = datetime.strptime('2002-01-06', '%Y-%M-%d').date()

x = []
y = []
with open('./final_data', 'r') as file:
    reader = csv.reader(file)
    reader.__next__()

    for line in reader:
        now = datetime.strptime(line[1], '%Y-%M-%d').date() - day0
        line[1] = now.days

        release = datetime.strptime(line[-1], '%Y-%M-%d').date() - day0
        line[-1] = release.days

        del(line[3])
        line = list(map(lambda x: float(x), line[1:]))
        x.append(line[:-1])
        y.append(line[-1])

x = np.array(x)
y = np.array(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Ridge: pretty tight around 77-78 range
# model = Ridge()

# Lasso: kinda wider range, 75-78
# model = Lasso()

# ElasticNet: similar to Ridge, 77-78
# model = ElasticNet()

# Decision Tree: 98??? Consistently
# model = tree.DecisionTreeRegressor()

model = RandomForestRegressor()

model.fit(x_train, y_train)
print(model.score(x_test,y_test))
