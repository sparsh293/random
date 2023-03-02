from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_servicecatalog as sc,
)

class S3BucketProduct(sc.ProductStack):
         def __init__(self, scope, id):
               super().__init__(scope, id)
               bucket = s3.Bucket(
               self,
              "MyBucket",
              removal_policy=RemovalPolicy.DESTROY,  # Destroy the bucket when the stack is deleted
              versioned=True,  # Enable versioning
              server_access_logs_bucket=s3.Bucket(
                     self, "MyBucketAccessLogs"
              ),  # Enable server access logging
              server_access_logs_prefix="logs/",
              )

               rule = bucket.add_lifecycle_rule(
               id="glacier-rule",
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

        

        product_from_stack = sc.CloudFormationProduct(self, "SCProduct_S3Bucket",
        product_name='S3', owner='CCOE',
        description='S3 Bucket',
        distributor='CCOE',
        product_versions = [sc.CloudFormationProductVersion(
              product_version_name="v1",
              cloud_formation_template=sc.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
        )]
        )

        my_portfolio_arn = "port-buc4l2zcpa67o"
        my_association = sc.CfnPortfolioProductAssociation(
        self, "MyAssociation",
        portfolio_id=my_portfolio_arn,
        product_id=product_from_stack.product_id
       )
