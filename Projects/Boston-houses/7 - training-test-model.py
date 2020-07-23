import sagemaker
import sagemaker
from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri

# This is an object that represents the SageMaker session that we are currently operating in. This
# object contains some useful information that we will need to access later such as our region.
session = sagemaker.Session()

# We need to retrieve the location of the container which is provided by Amazon for using XGBoost.
# As a matter of convenience, the training and inference code both use the same container.
container = get_image_uri(session.boto_region_name, 'xgboost')

# This is an object that represents the IAM role that we are currently assigned. When we construct
# and launch the training job later we will need to tell it what IAM role it should have. Since our
# use case is relatively simple we will simply assign the training job the role we currently have.
role = get_execution_role()


""""
(role, train_instance_count, train_instance_type, train_volume_size=30, train_volume_kms_key=None, 
train_max_run=86400, input_mode='File', output_path=None, output_kms_key=None, base_job_name=None, 
sagemaker_session=None, tags=None, subnets=None, security_group_ids=None, model_uri=None, 
model_channel_name='model', metric_definitions=None, encrypt_inter_container_traffic=False, 
train_use_spot_instances=False, train_max_wait=None, checkpoint_s3_uri=None, checkpoint_local_path=None

""""
# First we create a SageMaker estimator object for our model.
xgb = sagemaker.estimator.Estimator(container, # The location of the container we wish to use
                                    role,                                    # What is our current IAM Role
                                    train_instance_count=1,                  # How many compute instances
                                    train_instance_type='ml.m4.xlarge',      # What kind of compute instances
                                    output_path='s3://{}/{}/output'.format(session.default_bucket(), prefix),
                                    sagemaker_session=session)


# And then set the algorithm specific parameters.
xgb.set_hyperparameters(max_depth=5,
                        eta=0.2,
                        gamma=4,
                        min_child_weight=6,
                        subsample=0.8,
                        silent=0,
                        objective='binary:logistic',
                        early_stopping_rounds=10,
                        num_round=500)


# attach the training and validation datasets 
s3_input_train = sagemaker.s3_input(s3_data=train_location, content_type='csv')
s3_input_validation = sagemaker.s3_input(s3_data=val_location, content_type='csv')

# input is a map of train and validateion data
# Train a model using the input training dataset.
# you can call the deploy() method to host the model using the Amazon SageMaker hosting services
xgb.fit({'train': s3_input_train, 'validation': s3_input_validation})


# Return a Transformer that uses a SageMaker Model based on the training job.
# It reuses the SageMaker Session and base job name used by the Estimator.
xgb_transformer = xgb.transformer(instance_count = 1, instance_type = 'ml.m4.xlarge')

# Start a new transform job.
# test_location on S3
xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')

# check transform job is finished or not as it runs on background
xgb_transformer.wait()

# copy the output to local directory
!aws s3 cp --recursive $xgb_transformer.output_path $data_dir