#Dimensionality Reduction

""""
The *record_set* function in the SageMaker PCA model converts a numpy array 
into a **RecordSet** format that is the required format for the training input data.
This is a requirement for _all_ of SageMaker's built-in models. 
The use of this data type is one of the reasons that allows training of models 
within Amazon SageMaker to perform faster, especially for large datasets.
""""

from sagemaker import get_execution_role

# define a PCA model
from sagemaker import PCA


session = sagemaker.Session() # store the current SageMaker session

# get IAM role
role = get_execution_role()

print(role)

# this is current features - 1
# you'll select only a portion of these to use, later
N_COMPONENTS=33

pca_SM = PCA(role=role,
             train_instance_count=1,
             train_instance_type='ml.c4.xlarge',
             output_path=output_path, # specified, above
             num_components=N_COMPONENTS, 
             sagemaker_session=session)

# convert df to np array
train_data_np = counties_scaled.values.astype('float32')

# convert to RecordSet format
formatted_train_data = pca_SM.record_set(train_data_np)

# Train the model

%%time

# train the PCA mode on the formatted data
pca_SM.fit(formatted_train_data)

# Get the name of the training job, it's suggested that you copy-paste
# from the notebook or from a specific job in the AWS console

training_job_name='pca-2020-07-23-14-38-47-574'

# where the model is saved, by default
model_key = os.path.join(prefix, training_job_name, 'output/model.tar.gz')
print(model_key)

# download and unzip model
boto3.resource('s3').Bucket(bucket_name).download_file(model_key, 'model.tar.gz')

# unzipping as model_algo-1
os.system('tar -zxvf model.tar.gz')
os.system('unzip model_algo-1')

""""
Many of the Amazon SageMaker algorithms use MXNet for computational speed, 
including PCA, and so the model artifacts are stored as an array. After the 
model is unzipped and decompressed, we can load the array using MXNet.
""""
import mxnet as mx

# loading the unzipped artifacts
pca_model_params = mx.ndarray.load('model_algo-1')

# what are the params
""""
mean: The mean that was subtracted from a component in order to center it.
v: The makeup of the principal components; (same as ‘components_’ in an sklearn PCA model).
s: The singular values of the components for the PCA transformation. This does not exactly give the % variance from the original feature space, but can give the % variance from the projected feature space.
""""
print(pca_model_params)


# get selected params
s=pd.DataFrame(pca_model_params['s'].asnumpy())

v=pd.DataFrame(pca_model_params['v'].asnumpy())
v


# Calculate the explained variance for the top n principal components
# you may assume you have access to the global var N_COMPONENTS
def explained_variance(s, n_top_components):
    '''Calculates the approx. data variance that n_top_components captures.
       :param s: A dataframe of singular values for top components; 
           the top value is in the last row.
       :param n_top_components: An integer, the number of top components to use.
       :return: The expected data variance covered by the n_top_components.'''
    
    # get start idx just like above
    start_idx = N_COMPONENTS - n_top_components
    
    #calculate variance
    upper = np.sum(np.square(s.iloc[start_idx:,0]))
    lower = np.sum(np.square(s.iloc[:,0]))
    
    return upper/lower 
    # your code here
    
    pass

# test cell
n_top_components = 7 # select a value for the number of top components

# calculate the explained variance
exp_variance = explained_variance(s, n_top_components)
print('Explained variance: ', exp_variance)

""""
We can now examine the makeup of each PCA component based on the weightings of the original features 
hat are included in the component. The following code shows the feature-level makeup of the first component.

Note that the components are again ordered from smallest to largest and 
so I am getting the correct rows by calling N_COMPONENTS-1 to get the top, 1, component.
""""

import seaborn as sns

def display_component(v, features_list, component_num, n_weights=10):
    
    # get index of component (last row - component_num)
    row_idx = N_COMPONENTS-component_num

    # get the list of weights from a row in v, dataframe
    v_1_row = v.iloc[:, row_idx]
    v_1 = np.squeeze(v_1_row.values)
    # match weights to features in counties_scaled dataframe, using list comporehension
    comps = pd.DataFrame(list(zip(v_1, features_list)), 
                         columns=['weights', 'features'])
    # we'll want to sort by the largest n_weights
    # weights can be neg/pos and we'll sort by magnitude
    comps['abs_weights']=comps['weights'].apply(lambda x: np.abs(x))
    sorted_weight_data = comps.sort_values('abs_weights', ascending=False).head(n_weights)
    # display using seaborn
    ax=plt.subplots(figsize=(10,6))
    ax=sns.barplot(data=sorted_weight_data, 
                   x="weights", 
                   y="features", 
                   palette="Blues_d")
    ax.set_title("PCA Component Makeup, Component #" + str(component_num))
    plt.show()

# Deploying the PCA Model
    
%%time
# this takes a little while, around 7mins
pca_predictor = pca_SM.deploy(initial_instance_count=1, 
                              instance_type='ml.t2.medium')    