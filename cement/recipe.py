import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning) #annoying warning in pandas
pd.options.mode.chained_assignment = None #annoying warning in pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn import linear_model
from sklearn import preprocessing
from itertools import product
import matplotlib.pyplot as plt


def transform_data_for_model(df):
    #df=df[df['Age']==28]
    

    #assumption of what to do with na data for now
    df=df.fillna(0)

    #separate result data
    y=df['MPa']
    df=df.drop('MPa', axis=1)
    # df=df.drop(['Blast Furnace Slag', 'Superplasticizer'], axis=1)
    #columns for analysis
    df['ln_Age']=np.log(df['Age'])
    df=df.drop('Age', axis=1)

    mat_cols=df.columns[~df.columns.str.contains('Age')]
    # df['sum_mat']=df[mat_cols].sum(axis=1)
    # for col in mat_cols:
    #     name_col=col+'_ratio'
    #     df[name_col]=df[col]/df['sum_mat']
    #     df=df.drop(col, axis=1)
    
    df['water_cement_ratio']=df['Water']/df['Cement']
    #df=df.drop('sum_mat', axis=1)
    # Remove name of columns for easy use
    # materials.columns=list(map(str,range(len(mat_cols))))
    # 
    #materials = materials.apply(zscore)

    #generate interaction columns

    num_cols=df.columns
    # col1=num_cols
    # col2=num_cols
    # for i in product(col1,col2):
    #     name="*".join(i)
    #     df[name]=df[list(i)].prod(axis=1)
    x=df.copy()
    #normalize data
    #x=preprocessing.normalize(x,norm='l1')
    return x, y

def create_model(x,y):
    #split into test and train data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)# Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x_train, y_train)

    #y_pred = regr.predict(x_test)
    # The coefficients
    #print(x.columns)
    #print("Coefficients: \n", regr.coef_)
    # # The mean squared error
    #print("Mean absolute error: %.2f MPa" % mean_absolute_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    #print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

    # Plot outputs
    #plt.scatter(y_pred, y_test, color="black")
    #plt.xticks(())
    #plt.yticks(())

    #plt.show()
    return regr


def pullData(csv):
    df=pd.read_csv(csv)
    return

# Get Model
df=pd.read_csv('concrete-data.csv')
(x,y)=transform_data_for_model(df)
model=create_model(x,y)

run_model=False

if run_model:
    # Apply Model to Data
    df_in=pd.read_csv('input-data.csv')
    (x_in,y_in)=transform_data_for_model(df_in)
    pred_y_in=model.predict(x_in)
    df_in['Predicted MPa']=pred_y_in
    df_in.to_csv('output-data.csv')
    print("Initial Model")
    print(df_in[['MPa','Predicted MPa']])

    #retrain model
    non_predic_cols=df_in.columns[:-1]
    df_in=df_in[non_predic_cols]
    full_data=pd.concat([df,df_in])
    (x_new,y_new)=transform_data_for_model(full_data)
    new_model=create_model(x_new,y_new)
    #repeat guess with new model
    new_pred_y_in=new_model.predict(x_in)
    df_in['Predicted MPa']=new_pred_y_in
    df_in.to_csv('output-data-new.csv')
    print("Updated Model")
    print(df_in[['MPa','Predicted MPa']])


number_runs=100
coef=[]
for run in range(0,number_runs):
    df=pd.read_csv('concrete-data.csv')
    (x,y)=transform_data_for_model(df)
    model=create_model(x,y)
    coef.append(list(model.coef_))
coef_df=pd.DataFrame(coef)
coef_df.columns=x.columns
print(coef_df.describe())