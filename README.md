# s3-lambda-workflow
在某些场景下需要合并小文件用于后续业务，但是Amazon S3本身不支持Append。本方案设计了一套基于StepFunctions和Lambda的方案解决用户问题，在此解决方案中我们当用户上传需要合并的S3对象列表后触发Lambda做文件检查并调用Step Functions来通过Lamdba进行合并（读取小文件内容然后重新写入到一个大文件中），合并的结果写入到DynamoDB中。
## 通过SAM部署
参考[文档](https://docs.aws.amazon.com/zh_cn/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)安装AWS SAM CLI，部署方式如下：
```shell
 sam build --use-container
 sam deploy --guided
 sam deploy
 ```
