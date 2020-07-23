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
print(pca_model_params)