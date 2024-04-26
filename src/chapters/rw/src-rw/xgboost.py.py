#%%
from xgboost import XGBClassifier
# read data
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=.2)
# create model instance
bst = XGBClassifier(n_estimators=2, max_depth=2, learning_rate=1, objective='binary:logistic')
# fit model
bst.fit(X_train, y_train)
# make predictions
preds = bst.predict(X_test)
# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def plot_decision_boundary(X, y, classifier, resolution=0.02):
    """
    Modified version of an implementation in
    Sebastian Raschka and Vahid Mirijalili,
    Python Machine Learning,
    2nd ed., 2017, Packt Publishing
    """
    markers = ('o', 's')
    colors = ('b', 'o')
    cmap = ListedColormap(colors)
    
    # define the grid
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
    np.arange(x2_min, x2_max, resolution))
    
    if classifier is not None:
        # for each grid point, predict the class
        lab = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        lab = lab.reshape(xx1.shape)
    
        # plot the decision regions
        plt.contourf(xx1, xx2, lab, alpha=0.3, cmap=cmap)
        plt.xlim(xx1.min(), xx1.max())
        plt.ylim(xx2.min(), xx2.max())
    
    # plot the data points
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0],
                    y=X[y == cl, 1],
                    alpha=0.8,
                    c=colors[idx],
                    marker=markers[idx],
                    label=f'Class {cl}')
        plt.xlabel('feature 1')
        plt.ylabel('feature 2')
        plt.legend()
# %%
# create some toy data
rng = np.random.default_rng(seed=0)
X = rng.standard_normal((30, 2))

# divide the data
y = np.where(X[:,0]*X[:,1] >= 0, 1, 0)

# plot the data
plot_decision_boundary(X, y, None)
plt.title('Toy data')
plt.show()
# %%
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(criterion='gini',
                            max_depth=3,
                            random_state=0)
dt.fit(X, y)
#%%
plot_decision_boundary(X, y, dt)
plt.title('Scikit-Learn Decision Tree')
plt.show()
# %%
