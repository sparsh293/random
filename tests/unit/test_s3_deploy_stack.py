import aws_cdk as core
import aws_cdk.assertions as assertions

from s3_deploy.s3_deploy_stack import S3DeployStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3_deploy/s3_deploy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3DeployStack(app, "s3-deploy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
