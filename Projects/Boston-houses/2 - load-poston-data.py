from sklearn.datasets import load_boston
import pandas as pd

boston = load_boston()

# Preparing and splitting the data

print(boston.data)

# 506 * 13
X = pd.DataFrame(boston.data, columns=boston.feature_names)

# 506 * 1
Y = pd.DataFrame(boston.target)

print(X)
print(Y)
