Following https://acloudguru.com/blog/engineering/deploying-a-containerized-flask-application-with-aws-ecs-and-docker

Steps to do only once
```
# Create Registry
aws ecr create-repository --repository-name summarizer
```

Repo I made for this project:
```
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-west-2:584437639733:repository/summarizer",
        "registryId": "584437639733",
        "repositoryName": "summarizer",
        "repositoryUri": "584437639733.dkr.ecr.us-west-2.amazonaws.com/summarizer",
        "createdAt": "2021-01-02T20:59:17-08:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

Do this each time want to deploy 
```
# Login
aws ecr get-login-password \
    --region us-west-2 \
| docker login \
    --username AWS \
    --password-stdin 584437639733.dkr.ecr.us-west-2.amazonaws.com
docker build -t summarizer
docker tag summarizer:latest 584437639733.dkr.ecr.us-west-2.amazonaws.com/summarizer
docker push 584437639733.dkr.ecr.us-west-2.amazonaws.com/summarizer
```
