"""
This file contains three functions:
    
        - get_params: to get hyperparameters combinations for the algorithms
        - max_score_for_each: to get the best score for each algorithm for each metric
        - get_combinations: to get the combinations of imputers, balancers, and algorithms that worked best for a given metric
        
The functions in this file are used to entire algorithm optimization process more efficient and automated.

"""


from itertools import product
import numpy as np
import pandas as pd


from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from imblearn.over_sampling import SMOTE,ADASYN
from smote_variants import MWMOTE

from sklearn.naive_bayes import GaussianNB 
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,BaggingClassifier

from imblearn.under_sampling import ClusterCentroids,AllKNN
from sklearn.impute import SimpleImputer, KNNImputer


def get_params(algoritm=None):
    
    
    """
    This functions is a container for all hyperparameters combinations for the algorithms.
    The only parameter is the algorithm name.
    
    The steps are (for each algorithm):
        - define the hyperparameters and their values in lists
        - create a list of lists where each list is a combination of hyperparameters (using itertools.product)
        - create a list of dictionaries where each dictionary is a hyperparameters combination (lambda function get_param_dict)
        - return the list of dictionaries
    
    
    Parameters:
    -----------
    algorithm: str
        The name of the algorithm. The default value is None. The name should be the same as the algorithm name in sklearn/xgboost.
        The opitions are:
            - LogisticRegression
            - DecisionTreeClassifier
            - SVC
            - KNeighborsClassifier
            - GaussianNB
            - RandomForestClassifier
            - GradientBoostingClassifier
            - BaggingClassifier
            - XGBClassifier (xgboost.XGBClassifier)
    Returns:
    --------
    list of dicts
        A list of dictionaries with hyperparameters combinates for the algorithm (list of dicts). 
        If the algorithm name is not valide (from the list above), a ValueError is raised.
    """
    
    
    
    
    
    # this lambda functions create a list of dictionaries for hyperparameters combinations
    get_param_dict = lambda names,params: [{names[j]:params_comb[j] for j in range(len(names))} for params_comb in params]
    
    match algoritm:
        case "LogisticRegression":
            
            log_penalties = ['l1', 'l2', 'elasticnet', None]
            log_Cs =  [0.1, .3, .5, 1]
            log_solvers = ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']
            log_max_iters = [100,1000,5000]
            log_l1_ratios = np.linspace(0.1,1,5,endpoint=True)



            log_params = list(product(log_penalties,log_Cs,log_solvers,log_max_iters,log_l1_ratios))
            log_params_names = ["penalty","C","solver","max_iter","l1_ratio"]

            log_params_dict = get_param_dict(log_params_names,log_params)
            
            return log_params_dict
        
        case "DecisionTreeClassifier":
            
            tree_criterion = ["gini", "entropy", "log_loss"]
            tree_splitter = ["best", "random"]
            tree_max_depth = [2,4,6,8]
            tree_min_samples_split = [11,21,31]
            tree_min_samples_leaf = [3,5,7]
            tree_max_features = [10,15,"sqrt", "log2"]
            tree_random_state = [123,None]

            tree_params = list(product(tree_criterion,tree_splitter,tree_max_depth,tree_min_samples_split,
                                            tree_min_samples_leaf,tree_max_features,tree_random_state))


            tree_params_names = ["criterion","splitter","max_depth","min_samples_split","min_samples_leaf","max_features","random_state"]


            tree_params_dict = get_param_dict(tree_params_names,tree_params)
            
            return tree_params_dict
        
        case "SVC":
            
    
            svm_C = [.3,.5,1.,2.]
            svm_kernel = ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']
            svm_degree = [2,3,4]
            svm_gamma = ['scale', 'auto']
            svm_coef0 = [0,.1,.3,.5]
            svm_decision_function_shape = ['ovo', 'ovr']
            svm_random_state = [123,None]
            
            svm_params = list(product(svm_C,svm_kernel,svm_degree,svm_gamma,svm_coef0,svm_decision_function_shape,svm_random_state))
            svm_params_names = ["C","kernel","degree","gamma","coef0","decision_function_shape","random_state"]
            
            svm_params_dict = get_param_dict(svm_params_names,svm_params)
            
            return svm_params_dict
        
        case "KNeighborsClassifier":
            
            
            knn_n_neighbors = [5,7,10]
            knn_weights = ['uniform', 'distance']
            knn_algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
            knn_p = [1,2,3]
            
            knn_params =list(product(knn_n_neighbors,knn_weights,knn_algorithm,knn_p))
            knn_params_names = ['n_neighbors','weights','algorithm','p']
            
            knn_params_dict = get_param_dict(knn_params_names,knn_params)

            
            return knn_params_dict
        
        case "RandomForestClassifier":
            
            forest_n_estimators = [50,100,150]
            forest_criterion = ['gini','entropy','log_loss']
            forest_max_features = ['sqrt','log2',None]
            forest_min_samples_split = [2,4,6]
            forest_min_samples_leaf = [1,2,3]
            
            forest_params =list(product(forest_n_estimators,forest_criterion,forest_max_features,forest_min_samples_split,forest_min_samples_leaf))
            forest_params_names = ['n_estimators','criterion','max_features','min_samples_split','min_samples_leaf']
            
            forest_params_dict = get_param_dict(forest_params_names,forest_params)


            return forest_params_dict
        
        case "GradientBoostingClassifier":
            
            gradient_loss = ['log_loss','exponential']
            gradient_learning_rate = [.05,.1,.15]
            gradient_n_estimators = [50,100,150]
            gradient_subsample = [.3,.5,1]
            gradient_criterion = ['friedman_mse', 'squared_error']
            gradient_max_features = ['sqrt', 'log2',None]
            gradient_min_samples_split = [2,4,6]
            gradient_min_samples_leaf = [1,2,3]
            
            gradient_params =list(product(gradient_loss,gradient_learning_rate,gradient_n_estimators,\
                                    gradient_subsample,gradient_criterion,gradient_max_features,gradient_min_samples_split,gradient_min_samples_leaf))
            gradient_params_names = ['loss','learning_rate','n_estimators','subsample','criterion','max_features','min_samples_split','min_samples_leaf']
            
            gradient_params_dict = get_param_dict(gradient_params_names,gradient_params)


            return gradient_params_dict
        
        case "BaggingClassifier":
            
            bagging_n_estimators = [5,10,15,100]
            bagging_oob_score = [True,False]
            bagging_bootstrap_features = [True,False]
            
            
            bagging_params =list(product(bagging_n_estimators,bagging_oob_score,bagging_bootstrap_features))
            bagging_params_names = ['n_estimators','oob_score','bootstrap_features']
            
            bagging_params_dict = get_param_dict(bagging_params_names,bagging_params)
            
            return bagging_params_dict

        case "XGBClassifier":
            
            xg_n_estimators = [50,100,150,200] 
            xg_learning_rate = [.1,.04,0.2]
            xg_subsample = [.5,1,.3]
            xg_max_depth = [3,5,7,10]
            xg_max_leaves = [3,5,7,0]
            
            xg_params =list(product(xg_n_estimators,xg_learning_rate,xg_subsample,xg_max_depth,xg_max_leaves))
            xg_params_names = ['n_estimators','learning_rate','subsample','max_depth','max_leaves']
            
            xg_params_dict= get_param_dict(xg_params_names,xg_params)
            
            return xg_params_dict
        
        case "GaussianNB":
            
            naive_priors = None
            naive_var_smoothing  = 1e-9
            
            return [{'priors':naive_priors,'var_smoothing':naive_var_smoothing}]
            

        case _:
            
            raise ValueError("The algorithm name is not valid. \nPlease provide a valid algorithm name from the following list:\
                \n\t['LogisticRegression', 'DecisionTreeClassifier', 'SVC', 'KNeighborsClassifier',\
                'GaussianNB','RandomForestClassifier','GradientBoostingClassifier','BaggingClassifier','XGBClassifier']")





def max_score_for_each(df,by=['Algorithm','Metric'],set_='Test'):


    """
    This function returns the best score for each algorithm for each metric.
    The function groups the data by the 'by' parameter(s) and then gets the maximum score for each group.
    
    Parameters:
    -----------
    df: pd.DataFrame
        The dataframe with the results.
    by: list
        The columns to group by. The default value is ['Algorithm','Metric'].
    set_: str
        The set to get the best score. The default value is 'Test'.
        
    Returns:
    --------
    pd.DataFrame
        A dataframe with the best score for each algorithm for each metric.    
    
    """

    get_max_score = lambda group: group.loc[group['Score'].idxmax()]

    df_set = df[df['Set'] == set_]
    max_scores = df_set.groupby(by).apply(get_max_score).reset_index(drop=True)

    return max_scores




def get_combinations(performance_path = './results/general/full_data_performances_9_models_5_balancers.csv',df=None,
                    by_features=['Algorithm','Metric'],by_metric='AUC',by_set='Test',return_dict=False):
    
    
    """
    This function returns the combinations of algorithm, imputers, and balancers that worked best for a given metric.
    
    The steps are:
        - read the performance data (in cartesian product format, which means that each algorithm has all the combinations of imputers and balancers)
        - get the best score for each algorithm for each metric (using max_score_for_each function from this file)
        - filter the data by the given metric: this is the metric that we consider the primary metric to get the best combinations
        - use predefiend dictionaries to map the algorithm, imputer, and balancer names to the classes: this is 
            necessary to convert strings to classes, so enable the use of the classes in the pipeline
        - crete a list of lists: the length of the list is equal to the numbder of algorithms, 
            and each lists consists of [algorithm, [num_imputer_name,num_imputer,cat_imputer_name,cat_imputer],balancer]]
            the algorithm and balancer are classes, but the imputers are tuples with the name and the instantiated class
        - return the list of lists
        
        
    Parameters:
    -----------
    performance_path: str
        The path to the performance data. The default value is './results/general/full_data_performances_9_models_5_balancers.csv'.
    df: pd.DataFrame
        The dataframe with the performance data. The default value is None.
        
        if both performance_path and df are None, the error is raised.
        
    by_features: list
        The columns to group by. The default value is ['Algorithm','Metric'].
    by_metric: str
        The metric to consider while choosing the best performed combinations. The default value is 'AUC'.
    by_set: str
        The set to get the best score. The default value is 'Test'.
    return_dict: bool
        If True, the function returns a dictionary with the algorithms as keys. The default value is False.
        
    Returns:
    --------
    list of lists
        A list of lists with the best combinations of algorithm, imputer, and balancer for a given metric.
    """
    
    imputer_map = {
        'KNNImptuer':KNNImputer(),
        'SimpleImputer_mode':SimpleImputer(strategy='most_frequent'),
        'SimpleImputer_mean': SimpleImputer()
    }

    algorithm_map = {
    'NaiveBayes':GaussianNB,
    'KNN':KNeighborsClassifier,
    'DecisionTree':DecisionTreeClassifier,
    'LogisticRegression':LogisticRegression,
    'Bagging':BaggingClassifier,
    'SVM':SVC,
    'RandomForest':RandomForestClassifier,
    'XGBoost':XGBClassifier,
    'GradientBoosting':GradientBoostingClassifier
    }

    balancer_map = {
        "SMOTE":SMOTE,
        "MWMOTE":MWMOTE,
        "OriginalData":None,
        "ClusterCentroids":ClusterCentroids,
        "AllKNN":AllKNN,
        "ADASYN":ADASYN
    }
    
    if df is None:
        df = pd.read_csv(performance_path)
        
    
    data = max_score_for_each(df,by=by_features,set_=by_set)
    
    data = data[data['MainMetric'] == by_metric]
    
    data.reset_index(drop=True,inplace=True)
    
    
    hyper_dict = data[['Algorithm','Imputer','Imbalance']].to_dict()
    hyper_dict = {key.lower():list(value.values()) for key,value in hyper_dict.items()}

    hyper_dict['imputer'] = [im.split("__") for im in hyper_dict['imputer']]
    hyper_dict['imputer'] = [[imp[0],imputer_map[imp[0]],imp[1],imputer_map[imp[1]]] for imp in hyper_dict['imputer']]
    hyper_dict['imbalance'] = [balancer_map[val] for val in hyper_dict['imbalance']]
    hyper_dict['algorithm'] = [algorithm_map[alg] for alg in hyper_dict['algorithm']]

    combinations = [[hyper_dict[key][i] for key in hyper_dict] for i in range(len(hyper_dict['algorithm']))]
    
    combinations_dict = {combinations[i][0].__name__:combinations[i] for i in range(len(combinations))}
    
    
    if return_dict:
        return combinations_dict
    
    return combinations

    
