from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_servicecatalog as sc,
)
from aws_cdk.aws_servicecatalog import(
      Portfolio
)

class S3BucketProduct(sc.ProductStack):  #class for defining a s3 bucket ProductStack is the parent class
         def __init__(self, scope, id):  #constructor for S3BucketProduct class
               super().__init__(scope, id)  #method to call the constructor of parent class which returns the object of parent class and we can then use the methods of parent class
               bucket = s3.Bucket(          #aws construct for creating a s3 bucket
               self,                        #refersto the current instance of the class
              "MyBucket",                   #name of bucket
              removal_policy=RemovalPolicy.DESTROY,  # Destroy the bucket when the stack is deleted
              versioned=False,  # Enable versioning
              server_access_logs_bucket=s3.Bucket(
                     self, "MyBucketAccessLogs"
              ),  # Enable server access logging
              server_access_logs_prefix="logs/",
              )

               rule = bucket.add_lifecycle_rule(
               id="lifecycle-rule",
               prefix="",
               enabled=True,
               transitions=[
                s3.Transition(
                     transition_after=Duration.days(0),
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING
                )
            ]
        )
               


class S3DeployStack(Stack):

       def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        

        product_from_stack = sc.CloudFormationProduct(self, "SCProduct_S3Bucket", #aws construct for creating a cloudformation product
        product_name='S3', owner='CCOE',
        description='S3 Bucket',
        distributor='CCOE',
        product_versions = [sc.CloudFormationProductVersion(    #aws construct for defining the product version and also initialising the S3BucketProduct class and creating a cf template through it
              product_version_name="v1",
              cloud_formation_template=sc.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
        )]
        )



        
