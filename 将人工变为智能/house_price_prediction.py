# Utility packages
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

# Preprocessing related Imports
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, LabelBinarizer, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin

# Regressors
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedShuffleSplit, RandomizedSearchCV
from xgboost import XGBRegressor
import os
# Metrics
from sklearn.metrics import mean_squared_error

if __name__ == '__main__':
    train = pd.read_csv(os.path.join('~/s3data/dataset', 'train.csv')).drop("ADDRESS", axis=1)
    test = pd.read_csv(os.path.join('~/s3data/dataset', 'test.csv')).drop("ADDRESS", axis=1)
    
    # analysize data
    train.head()

    train.info()

    train.describe()

    train.hist(bins=50, figsize=(15, 20))

    train.corr()["TARGET(PRICE_IN_LACS)"]
    

    # 分层抽样以消除抽样偏差
    train["bhk_cat"] = np.ceil(train["BHK_NO."] / 1.5)
    train["bhk_cat"].where(train["bhk_cat"] < 5, 5, inplace=True)
    split = StratifiedShuffleSplit(n_splits=1, test_size=.2, random_state=42)
    for train1, test1 in split.split(train, train['bhk_cat'], train['BHK_OR_RK']):
        strat_train = train.loc[train1]
        strat_test = train.loc[test1]

    print("TRAIN RATIOS \n", strat_train["BHK_OR_RK"].value_counts() / len(strat_train["BHK_OR_RK"]))
    print("TEST RATIOS \n", strat_test["BHK_OR_RK"].value_counts() / len(strat_test["BHK_OR_RK"]))

    print("TRAIN RATIOS \n", strat_train["bhk_cat"].value_counts() / len(strat_train["bhk_cat"]))
    print("TEST RATIOS \n", strat_test["bhk_cat"].value_counts() / len(strat_test["bhk_cat"]))

    for set in (strat_train, strat_test):
        set.drop(["bhk_cat"], axis=1, inplace=True)
    
    copied = strat_train.copy()
    # 经纬度散点图了解地理属性与目标变量的关系
    copied.plot(kind='scatter', x='LONGITUDE', y='LATITUDE', alpha=0.4, c="TARGET(PRICE_IN_LACS)", cmap=plt.get_cmap("jet"),
                colorbar=True)

    scatter_matrix(copied, figsize=(20, 20))

    copied[copied["SQUARE_FT"] < 2000000].plot(kind='scatter', x="SQUARE_FT", y="TARGET(PRICE_IN_LACS)", s="BHK_NO.",
                                               label="BHK_NO.", c="RESALE", cmap=plt.get_cmap("jet"), colorbar=True)
    plt.legend()
    
    # 准备用于模型训练的data
    attribute_data = strat_train.drop("TARGET(PRICE_IN_LACS)", axis=1)
    label_data = strat_train["TARGET(PRICE_IN_LACS)"]

    # 创建单独预处理数值和分类属性的管道
    num_attribs = ['BHK_NO.', 'SQUARE_FT', 'LONGITUDE', 'LATITUDE']
    cat_attribs = ['UNDER_CONSTRUCTION', 'RERA', 'READY_TO_MOVE', 'RESALE']
    string_cat_attribs = ['POSTED_BY', 'BHK_OR_RK']


    class DataFrameSelector(BaseEstimator, TransformerMixin):
        def __init__(self, attribute_names):
            self.attribute_names = attribute_names

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return X[self.attribute_names].values


    class CustomLabelBinarizer(BaseEstimator, TransformerMixin):
        def __init__(self, sparse_output=False):
            self.sparse_output = sparse_output

        def fit(self, X, y=None):
            return self

        def transform(self, X, y=None):
            enc = LabelBinarizer(sparse_output=self.sparse_output)
            return enc.fit_transform(X)


    num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),
        ('std', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('selector', DataFrameSelector(cat_attribs)),
        ('Binarizer', CustomLabelBinarizer(sparse_output=True))
    ])
    string_cat_pipeline = Pipeline([
        ('selector', DataFrameSelector(string_cat_attribs)),
        ('Binarizer', OneHotEncoder())
    ])
    finalPipeline = FeatureUnion(transformer_list=[
        ("num_pipeline", num_pipeline),
        ("cat_pipeline", cat_pipeline),
        ("string_cat_pipeline", string_cat_pipeline),
    ])

    attribute_data_corrected = finalPipeline.fit_transform(attribute_data)


    # Functions for analysing the performance
    def MSE(model, inp, out):
        housing_predicted = model.predict(inp)
        return np.sqrt(mean_squared_error(out, housing_predicted))



    # 用xgboost进行训练

    param_grid = [
        {'n_estimators': [270, 280, 300], 'max_depth': [5], 'reg_lambda': [0.9, 1, 1.1],
         'learning_rate': [0.01, 0.05, 0.1],
         'gamma': [0.9, 1, 1.1], 'reg_alpha': [0.9, 1, 1.1], 'booster': ['dart']}]

    XGB_REG = XGBRegressor(random_state=1, objective='reg:squarederror')

    XGBR = RandomizedSearchCV(XGB_REG, param_grid, cv=5, verbose=5,
                              scoring='neg_mean_squared_error', random_state=1, n_iter=900, n_jobs=4)
    XGBR.fit(attribute_data_corrected.toarray(), label_data)
    XGB_REG = XGBR.best_estimator_
    # xgb模型保存
    import joblib
    joblib.dump(XGB_REG, 'xgb.pkl', compress=3)
    # 用切分的测试集计算MSE
    test_attribute_data = strat_test.drop("TARGET(PRICE_IN_LACS)", axis=1)
    test_label_data = strat_test["TARGET(PRICE_IN_LACS)"]

    test_attribute_data_corrected = finalPipeline.transform(test_attribute_data)
    print("Extreme Gradient Boosted Regressor MSE: ",
          MSE(XGB_REG, test_attribute_data_corrected.toarray(), test_label_data))

    # 预测并输出
    FINAL_test=finalPipeline.transform(test)
    target=pd.DataFrame(XGB_REG.predict(FINAL_test))
    test["TARGET(PRICE_IN_LACS)"]=target
    print(test.head())
    test.to_csv("prediction.csv")
