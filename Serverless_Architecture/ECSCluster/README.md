# Cloud-Native Application architecture: ECS Cluster

<br>

This repository provides a <mark>**Cloud-Native Application Architecture**</mark> using AWS Serverless Application Model (🟠**SAM**).  
It leverages 🟠**AWS Fargate** to run containers in a `cost-effective`, `reliable`, and `scalable` manner, eliminating the need for server management.

The architecture follows a `SEC01-BP06`: <mark>**Immutable Infrastructure**</mark> approach with Infrastructure as Code (**`IaC`**) and Configuration as Code (**`CaC`**), ensuring consistency and repeatability in deployments.  
It adopts a **modular strategy**, allowing `flexible deployment` and management of individual components while adhering to the <mark>**AWS Well-Architected Framework**</mark> **best practices**.🫶🏻 [^1]

This solution is designed to support **education and testing environments**, providing a structured, scalable, and automated infrastructure-as-code setup.

---

<br>

## 🪩 Table of Contents

<br>

- [Cloud-Native Application architecture: ECS Cluster](#cloud-native-application-architecture-ecs-cluster)
  - [🪩 Table of Contents](#-table-of-contents)
  - [🪩 Architecture Overview](#-architecture-overview)
    - [☻ About Deployment strategy](#-about-deployment-strategy)
    - [☻ Deployment Order](#-deployment-order)
  - [🪩 Deployment Steps](#-deployment-steps)
    - [☻ Requirements](#-requirements)
      - [✰ Python modules](#-python-modules)
      - [✰ AWS PoLP Permissions for a workforce as a deployer](#-aws-polp-permissions-for-a-workforce-as-a-deployer)
    - [0️⃣ **Create a Virtual Environment** (Recommended)](#0️⃣-create-a-virtual-environment-recommended)
    - [1️⃣ **\[Manual Pre-steps\]**](#1️⃣-manual-pre-steps)
      - [✰ 🐾 A. **🔴ACM - Upload TLS Certificates**](#--a-acm---upload-tls-certificates)
      - [✰ 🐾 B. **Create Secure 🟢S3 Bucket for 🟠SAM Artifacts**](#--b-create-secure-s3-bucket-for-sam-artifacts)
        - [✦ 🐾 Create new 🟢S3 Bucket:](#--create-new-s3-bucket)
        - [✦ 🐾 Apply a 📄Secure Bucket Policy:](#--apply-a-secure-bucket-policy)
        - [✦ 🐾 Verify creation:](#--verify-creation)
      - [✰ 🐾 C. **Create new 🟠ECR Private Repo and Register new container image**](#--c-create-new-ecr-private-repo-and-register-new-container-image)
        - [✦ 🐾 Create new 🟠ECR Private Repository:](#--create-new-ecr-private-repository)
        - [✦ 🐾 Register Application images:](#--register-application-images)
    - [2️⃣ **\[Deploy foundational infrastructure\]**](#2️⃣-deploy-foundational-infrastructure)
      - [✰ 🐾 A. **🔴SSM Parameter Store settings**](#--a-ssm-parameter-store-settings)
        - [✦ 🐾 (Optional): Verify creation:](#--optional-verify-creation)
      - [✰ 🐾 B. **Deploy Basic 🟣VPC**](#--b-deploy-basic-vpc)
        - [✦ 🐾 Create 🟣Networking:](#--create-networking)
        - [✦ 🐾 Update the values of 🔴SSM Parameter Store:](#--update-the-values-of-ssm-parameter-store)
        - [✦ 🐾 Verify creation:](#--verify-creation-1)
      - [✰ 🐾 C. **Deploy 🟣VPC-Extras💰**](#--c-deploy-vpc-extras)
      - [✰ 🐾 D. **Deploy 🟠Lambda for ALB Logs Forwarding \& 🟢S3**](#--d-deploy-lambda-for-alb-logs-forwarding--s3)
      - [✰ 🐾 E. **Deploy Internal 🔴ALB💰**](#--e-deploy-internal-alb)
      - [✰ 🐾 F. **Deploy 🟠ECS Cluster**](#--f-deploy-ecs-cluster)
    - [3️⃣ **\[Deploy initial 🟠ECS Service for 'Blue' environment\]**](#3️⃣-deploy-initial-ecs-service-for-blue-environment)
      - [✰ 🐾 A. **Deploy 🟠ECS Service \& 🟠Fargate💰**](#--a-deploy-ecs-service--fargate)
      - [✰ 🐾 B. **Deploy 🔴Application Auto Scaling**](#--b-deploy-application-auto-scaling)
    - [☻ **\[Test the Connection\]**](#-test-the-connection)
    - [4️⃣ (Option): **\[Deploy initial 🟠ECS Service for 'Green' environment\]**](#4️⃣-option-deploy-initial-ecs-service-for-green-environment)
    - [🚮 **Clean it up**](#-clean-it-up)
      - [✰ (Option): Check Actual Costs🫣](#-option-check-actual-costs)

---

<br>

## 🪩 Architecture Overview

<br>

The deployment is structured into **multiple modular 🟠SAM templates**, each responsible for a specific part of the infrastructure.  
The stack includes:

- 🟣**Networking** (VPC, Subnets, ACLs, RouteTables, Security Groups, Internet/NAT Gateway, VPC Endpoints(Gen.1 and 2))
- 🔴**SSM Parameter Store** for configuration management
- **Observability and logging**(ALBLogs-Forwarder(🟠**Lambda**, 🟢**S3**))  
- 🔴**Application Load Balancer** (ALB) for routing traffic
- 🟠**ECS Cluster** and 🔴**Application Auto Scaling** for serverless container workloads
- <i>Manual operations</i>:
  - 🔴**AWS Certificate Manager** (ACM) for provide End-to-End encrypt transit 

|High-level overview|
|---|
|![image](../../assets/FargateCluster-HighLevel-Overview.jpg)|

<details>

<summary>📖Details</summary>

|Details|
|---|
|![image](../../assets/FargateCluster-Overview.jpg)|

</details>

---

<br>

### ☻ About Deployment strategy

<br>

|🟠AWS SAM with 🔴SSM Parameter Store|
|---|
|![image](../../assets/FargateCluster-SSMPS.jpg)|

<br>

>🙄 Why 🔴**SSM Parameter Store** is Better than 🔴**CloudFormation** `Export`/`Import`?

Using CloudFormation Export/Import can lead to **operational chaos**🫠. Here’s why:

1. **Tightly Coupled Stacks:**
    - If you update or delete the stack exporting values, dependent stacks **break**.
    - You **cannot delete an export** while another stack imports it.
2. **Lack of Visibility:**
    - **No built-in tracking** of which stacks are consuming exported values.
    - Hard to manage across <mark>**multi-account**</mark> or <mark>**multi-region**</mark> setups.
3. **Deployment Order Problem:**
    - The **exporting stack** must always deploy **first**, and the **importing stack** only after.
    - **Rollback issues**: If the exporter fails, the importer cannot proceed.
4. **No Cross-Account/Region Support:**
    - `!ImportValue` works **only within the same account and region**.

<br>

>🙃 **Why Choose 🔴SSM Parameter Store?**

🔴**SSM Parameter Store** offers a **modern, flexible, and decoupled approach** to infrastructure deployments:

1. **Decoupled Stacks:**
    - SSM parameters act as a <mark>**centralized state**</mark>.
    - Stacks read from SSM without dependency on each other.
2. **Cross-Account/Region Support:**
    - SSM parameters can be accessed from <mark>**different accounts and regions**</mark> with proper permissions.
3. **Versioning & History:**
    - SSM provides **parameter versions**, simplifying rollbacks and troubleshooting.
4. **Real-Time Updates:**
    - Change the value **once** in SSM, and all consuming stacks will **automatically** use the updated value.

<br>

<u>🛠️ **Enhancements & Best Practices**</u>

1. <mark>**Centralized Parameter Store**</mark> (P.S.)
    - 🔒 **Encryption**: Use 🔴**AWS KMS** to encrypt sensitive parameters.
    - 💰 **Tier Selection**: Use the **Standard Tier** unless you need history, expiration, or policies.
    - 🔑 **Secure Access**: Restrict access with 🔴**IAM policies** like `ssm:GetParameter` and `ssm:GetParameterHistory`.
    - 📏 **Automation**: Use 🔴**AWS Config** to identify unencrypted parameters.
2. **Tagging for Simplicity:**
    - Tag parameters by **environment** (e.g., Dev, Staging, Prod) to simplify management and querying.

>💡 **Tip**: Always use the "String" type for stack parameters unless you specifically need "**SecureString**" or "**StringList**".

---

<br>

### ☻ Deployment Order

<br>

- To ensure dependencies are met, deploy the stacks in the following order:
  - 💸: **Pay-as-you-go**
  - ↪️: Partial nested-stacks

| yaml | purpose |
|---|---|
| 1. **SSM_PS.yaml** | Stores the basic parameters (e.g., VPC Name, Availability Zones...) in SSM Parameter Store. |
| 2. **Basic_VPC.yaml**<br>↪️ **VPC.yaml**<br>↪️ **SSM_PS_Update_VPC.yaml** | Creates the basic networking components and update dynamic values of it to the SSM P.S. |
| 3. **VPC_Extras_Gen2Endpoint.yaml**💸 | Adds additional networking resources like NAT Gateway and VPC Endpoints. |
| 4. **VPC_Extras_Flowlogs.yaml**💸 | Enables VPC Flow Logs for monitoring network traffic. |
| 5. **ALB_LogsForwarder.yaml** | Sets up forwarding of ALB access logs to S3 or another logging solution. (by Lambda) |
| 6. **ALB.yaml**💸<br>↪️ **ALB_Internal.yaml**<br>↪️ **SSM_PS_Update_ALB.yaml** | Deploys the internal ALB for routing requests within the VPC and update dynamic values of it to the SSM P.S. |
| 7. **ECS.yaml**<br>↪️ **ECSCluster.yaml**<br>↪️ **SSM_PS_Update_ECS.yaml** | Provisions the ECS Fargate cluster for running serverless containerized applications. |
| 8. **ECSService_Blue.yaml**💸<br>**ECSService_Green.yaml**💸 | Deploy serverless containerized applications as ECS Service. |
| 9. **AppAutoScaling.yaml**💸 | Configures application auto-scaling policies for Fargate tasks. |

<br>

```bash-session
### Always do validate an AWS SAM template before deploy it.🙃
# for val in *yaml ; do echo "[${val:-NULL}]" ; sam validate -t ${val} --lint ; echo ; done 
```

<details>

<summary>📖An example of output</summary>

>```console
>[ALB.yaml]
>~/ALB.yaml is a valid SAM Template
>
>[ALB_Internal.yaml]
>~/ALB_Internal.yaml is a valid SAM Template
>
>[ALB_LogsForwarder.yaml]
>~/ALB_LogsForwarder.yaml is a valid SAM Template
>
>[AppAutoScaling.yaml]
>~/AppAutoScaling.yaml is a valid SAM Template
>
>[Basic_VPC.yaml]
>~/Basic_VPC.yaml is a valid SAM Template
>
>[ECSCluster.yaml]
>~/ECSCluster.yaml is a valid SAM Template
>
>[SSM_PS.yaml]
>~/SSM_PS.yaml is a valid SAM Template
>
>[SSM_PS_Update_ALB.yaml]
>~/SSM_PS_Update_ALB.yaml is a valid SAM Template
>
>[SSM_PS_Update_VPC.yaml]
>~/SSM_PS_Update_VPC.yaml is a valid SAM Template
>
>[VPC.yaml]
>~/VPC.yaml is a valid SAM Template
>
>[VPC_Extras_Flowlogs.yaml]
>~/VPC_Extras_Flowlogs.yaml is a valid SAM Template
>
>[VPC_Extras_Gen2Endpoint.yaml]
>~/VPC_Extras_Gen2Endpoint.yaml is a valid SAM Template
>```

</details>

---

<br>

## 🪩 Deployment Steps

<br>

> 💡 **Note:**
> In this case, we’ll deploy this architecture in <mark>**us-west-2 (Oregon)**</mark>.

---

<br>

### ☻ Requirements

<br>

---

<br>

#### ✰ Python modules

<br>

- Python 3.12+
  - Boto3
  - botocore
  - aws-lambda-powertools
  - aws-xray-sdk

---

<br>

#### ✰ AWS PoLP Permissions for a workforce as a deployer

<br>

<details>

<summary>📖Principle of Least Privilege (PoLP) Policy</summary>

| Target Services | Minimum permissions | 
|---|---|
| 🔴**Application AutoScaling** | application-autoscaling:RegisterScalableTarget |
| | application-autoscaling:PutScalingPolicy |
| | application-autoscaling:DeregisterScalableTarget |
| | autoscaling-plans:CreateScalingPlan |
| | autoscaling-plans:UpdateScalingPlan |
| | autoscaling-plans:DeleteScalingPlan |
| 🔴**CloudFormation** | cloudformation:CreateStack |
| | cloudformation:UpdateStack |
| | cloudformation:DescribeStacks |
| | cloudformation:DeleteStack |
| 🔴**CloudWatch** | cloudwatch:PutMetricData |
| | cloudwatch:GetMetricData |
| | cloudwatch:GetMetricStatistics |
| | cloudwatch:DescribeAlarms |
| 🟠**EC2** | ec2:Describe* |
| | ec2:AuthorizeSecurityGroup* |
| | ec2:CreateSecurityGroup |
| | ec2:DeleteSecurityGroup |
| | ec2:CreateRoute* |
| | ec2:ReplaceRoute* |
| | ec2:AssociateRouteTable |
| | ec2:CreateTags |
| | ec2:AcceptVpcEndpointConnections |
| | ec2:CreateNetworkInterface* |
| | ec2:DeleteRoute* |
| | ec2:DeleteNetworkInterface* |
| | ec2:CreateVpcEndpoint* |
| | ec2:ModifyVpcEndpoint* |
| | ec2:DeleteVpcEndpoint* |
| 🟠**ECR** | ecr:GetAuthorizationToken |
| | ecr:BatchCheckLayerAvailability |
| | ecr:GetDownloadUrlForLayer |
| | ecr:BatchGetImage |
| 🟠**ECS** | ecs:CreateCluster |
| | ecs:CreateService |
| | ecs:DeleteService |
| | ecs:Describe* |
| | ecs:RegisterTaskDefinition |
| | ecs:RunTask |
| | ecs:StopTask |
| | ecs:UpdateService |
| 🟠**ALB** | elasticloadbalancing:CreateListener |
| | elasticloadbalancing:CreateLoadBalancer |
| | elasticloadbalancing:CreateTargetGroup |
| | elasticloadbalancing:Delete* |
| | elasticloadbalancing:DeregisterTargets |
| | elasticloadbalancing:Describe* |
| | elasticloadbalancing:RegisterTargets |
| 🟠**Lambda** | lambda:CreateFunction |
| | lambda:InvokeFunction |
| | lambda:UpdateFunctionConfiguration |
| | lambda:UpdateFunctionCode |
| | lambda:DeleteFunction |
| 🔴**CloudWatch Logs** | logs:Create* |
| | logs:Describe* |
| | logs:FilterLogEvents |
| | logs:Get* |
| | logs:List* |
| | logs:PutLogEvents |
| | logs:StartQuery |
| | logs:StopQuery |
| | logs:TagLogGroup |
| 🟢**S3** | s3-object-lambda:* |
| | s3:GetObject |
| | s3:PutObject |
| | s3:ListBucket |
| | s3:DeleteObject |
| | s3:GetBucketLocation |
| 🔴**SSM** | ssm:DescribeDocument |
| | ssm:GetAutomationExecution |
| | ssm:ListDocuments |
| | ssm:StartAutomationExecution |
| | tag:GetResources |
| 🔴**IAM** | iam:Generate* |
| | iam:Get* |
| | iam:List* |
| | iam:PassRole |
| | iam:Update* |
| | iam:Delete* |
| | iam:Upload* |
| | iam:CreateRole |
| | iam:CreatePolicy* |
| | iam:CreateServiceSpecificCredential |
| | iam:CreateServiceLinkedRole |
| | iam:Attach* |
| | iam:Put* |

</details>

---

<br>

### 0️⃣ **Create a Virtual Environment** (Recommended)

<br>

Before deploying AWS services, it’s **highly recommended** to create a **virtual environment**.  
This isolates dependencies required for this project from your **global Python environment**, preventing conflicts and keeping things clean.

<br>

📌 Clone the Repository & Set Up the Virtual Environment (**Using `venv` (Python 3.3+)**)

<br>

- 📌 e.g., <mark>**On 🔵CloudShell**</mark> (AWS managed network)

1. 🐾 **Navigate to your working directory & clone the repository:**

```bash-session
# cd /path/to/your/project
# git clone https://github.com/Hideki-Morita/aws-serverless-education.git
# cd serverless-education/Serverless_Architecture/ECSCluster
```

>```console
>Cloning into 'aws-serverless-education'...
>remote: Enumerating objects: 69, done.
>remote: Counting objects: 100% (69/69), done.
>remote: Compressing objects: 100% (41/41), done.
>remote: Total 69 (delta 22), reused 59 (delta 12), pack-reused 0 (from 0)
>Receiving objects: 100% (69/69), 885.91 KiB | 15.27 MiB/s, done.
>Resolving deltas: 100% (22/22), done.
>```

- Create a virtual environment:

```bash-session
# python3 -m venv awsvenv
```

<br>

2. 🐾 **Activate the virtual environment:**

  - 🐧 On macOS/Linux:

  ```bash-session
  # source awsvenv/bin/activate
  ```

  - 🪟 On Windows:

  ```ps1
  PS1> awsvenv\Scripts\activate
  ```

✅ Once activated, your terminal will show something like this:  

>```console
>(awsvenv) user@hostname:~/aws-serverless-education/Serverless_Architecture/ECSCluster$ 
>```

<br>

3. 🐾 **Install Required Dependencies:**

- With the virtual environment activated, install the required Python libraries for the 🟠**Lambda function**:

```bash-session
# pip install -r requirements.txt
```

<details>

<summary>📖An example of output</summary>

>```console
>Collecting boto3
>  Downloading boto3-1.36.21-py3-none-any.whl (139 kB)
>     |████████████████████████████████| 139 kB 3.6 MB/s            
>Collecting botocore
>  Downloading botocore-1.36.21-py3-none-any.whl (13.4 MB)
>     |████████████████████████████████| 13.4 MB 9.5 MB/s            
>Collecting aws-lambda-powertools
>  Downloading aws_lambda_powertools-3.6.0-py3-none-any.whl (768 kB)
>     |████████████████████████████████| 768 kB 85.6 MB/s            
>Collecting aws-xray-sdk
>  Downloading aws_xray_sdk-2.14.0-py2.py3-none-any.whl (101 kB)
>     |████████████████████████████████| 101 kB 10.3 MB/s           
>Collecting s3transfer<0.12.0,>=0.11.0
>  Downloading s3transfer-0.11.2-py3-none-any.whl (84 kB)
>     |████████████████████████████████| 84 kB 4.4 MB/s             
>Collecting jmespath<2.0.0,>=0.7.1
>  Downloading jmespath-1.0.1-py3-none-any.whl (20 kB)
>Collecting urllib3<1.27,>=1.25.4
>  Downloading urllib3-1.26.20-py2.py3-none-any.whl (144 kB)
>     |████████████████████████████████| 144 kB 9.9 MB/s            
>Collecting python-dateutil<3.0.0,>=2.1
>  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
>     |████████████████████████████████| 229 kB 21.7 MB/s            
>Collecting typing-extensions<5.0.0,>=4.11.0
>  Downloading typing_extensions-4.12.2-py3-none-any.whl (37 kB)
>Collecting wrapt
>  Downloading wrapt-1.17.2-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (82 kB)
>     |████████████████████████████████| 82 kB 1.3 MB/s             
>Collecting six>=1.5
>  Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
>Installing collected packages: six, urllib3, python-dateutil, jmespath, botocore, wrapt, typing-extensions, s3transfer, boto3, aws-xray-sdk, >aws-lambda-powertools
>Successfully installed aws-lambda-powertools-3.6.0 aws-xray-sdk-2.14.0 boto3-1.36.21 botocore-1.36.21 jmespath-1.0.1 python-dateutil-2.9.0.post0 >s3transfer-0.11.2 six-1.17.0 typing-extensions-4.12.2 urllib3-1.26.20 wrapt-1.17.2
>WARNING: You are using pip version 21.3.1; however, version 25.0.1 is available.
>You should consider upgrading via the '/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/ECSCluster/awsvenv/bin/>python3 -m pip install --upgrade pip' command.
>```

</details>

<br>

4. 🐾 **Verify Installation:**

- (Optional) Check installed packages:

```bash-session
# pip list
```

✅ You should see `boto3`, `aws-lambda-powertools`, and `aws-xray-sdk` in the output.

>```console
>Package               Version
>--------------------- -----------
>aws_lambda_powertools 3.6.0
>aws-xray-sdk          2.14.0
>boto3                 1.36.21
>botocore              1.36.21
>jmespath              1.0.1
>pip                   21.3.1
>python-dateutil       2.9.0.post0
>s3transfer            0.11.2
>setuptools            59.6.0
>six                   1.17.0
>typing_extensions     4.12.2
>urllib3               1.26.20
>wrapt                 1.17.2
>WARNING: You are using pip version 21.3.1; however, version 25.0.1 is available.
>You should consider upgrading via the '/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/ECSCluster/awsvenv/bin/>python3 -m pip install --upgrade pip' command
>```

---

<br>

### 1️⃣ **[Manual Pre-steps]**

<br>

---

<br>

#### ✰ 🐾 A. **🔴ACM - Upload TLS Certificates**

- 📌 Example Files:
  - **Root Certificate**: <i>certificate.crt</i>  
  - **Child Certificate**: <i>child_certificate.crt</i>  
  - **Child Private Key**: <i>child_private_key.pem</i>  

<details>

<summary>📖Summary of Certificates</summary>

- **Key algorithm**
  - **EC** with **P-256 curve**

- **certificate.crt (Root Certificate)**
  - issuer=CN=masermind.tsclowning.com
  - subject=CN=masermind.tsclowning.com
  - notBefore=Mar 18 10:19:55 2025 GMT
  - notAfter=Apr  1 10:19:55 2029 GMT
  - No extensions in certificate

- **child_certificate.crt (Child Certificate)**
  - issuer=CN=masermind.tsclowning.com
  - subject=CN=*.tsclowning.com
  - notBefore=Mar 18 10:22:18 2025 GMT
  - notAfter=Mar 18 10:22:18 2029 GMT
  - X509v3 Subject Alternative Name: 
  -     DNS:*.tsclowning.com, DNS:peter.tsclowning.com, DNS:wendy.tsclowning.com, DNS:betty.tsclowning.com, DNS:james.tsclowning.com, DNS:inez.tsclowning.com, DNS:tsclowning.com
</details>

<br>

📌 e.g., <mark>**On 🔵CloudShell**</mark> (AWS managed network)

- Upload self-certificate to 🔴**ACM**

> 💡 **Note:**
> 🙃 The `schema` ensures binary-safe file uploads (`fileb://`)

```bash-session
# export AWS_DEFAULT_REGION=us-west-2
# aws acm import-certificate --certificate fileb://CAs/child_certificate.crt --private-key fileb://CAs/child_private_key.pem --certificate-chain fileb://CAs/certificate.crt
```

>```console
>{
>    "CertificateArn": "arn:aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877"
>}
>```

- (Option) Verify the uploaded certificate

```bash-session
# aws acm list-certificates --includes 'keyTypes=[EC_prime256v1]'
```

<details>

<summary>📖An example of output</summary>

>```json
>{
>  "CertificateSummaryList": [
>    {
>      "CertificateArn": "arn:aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877",
>      "DomainName": "*.swiftie.com",
>      "SubjectAlternativeNameSummaries": [
>        "*.swiftie.com",
>        "Betty.swiftie.com",
>        "James.swiftie.com",
>        "Inez.swiftie.com",
>        "swiftie.com"
>      ],
>      "HasAdditionalSubjectAlternativeNames": false,
>      "Status": "ISSUED",
>      "Type": "IMPORTED",
>      "KeyAlgorithm": "EC-prime256v1",
>      "KeyUsages": [
>        "ANY"
>      ],
>      "ExtendedKeyUsages": [
>        "NONE"
>      ],
>      "InUse": false,
>      "RenewalEligibility": "INELIGIBLE",
>      "NotBefore": "2025-02-15T11:15:00+00:00",
>      "NotAfter": "2029-02-14T11:15:00+00:00",
>      "CreatedAt": "2025-02-15T13:54:38.212000+00:00",
>      "ImportedAt": "2025-02-15T13:54:38.213000+00:00"
>    }
>  ]
>}
>```

</details>

---

<br>

#### ✰ 🐾 B. **Create Secure 🟢S3 Bucket for 🟠SAM Artifacts**

<br>

> 🙄Why create a custom 🟢**S3 Bucket** for 🟠**AWS SAM**?

By default, 🟠**AWS SAM** creates an 🟢**S3 Bucket** with a <u>predictable name</u>, like, <br> **aws-sam-cli-managed-default-samclisourcebucket**-xxxxxxxx.  

While convenient, this introduces potential risks:  
1. **Predictable Naming**: Attackers🤖 **could guess the bucket name** and target it with API requests.🫠
2. **Cost Risks**: Even failed requests incur AWS charges.💸
3. **Security Gaps**: The default bucket may not have strict policies, increasing the attack surface.

> 💡 To mitigate these risks, create a custom 🟢**S3 Bucket** with restrictive policies and encryption.

<br>

- [💡Tips: **General purpose 🟢S3 Bucket naming rules**](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html#create-bucket-name-guid) 
  - Useful commands for generate globally unique identifiers
  - **`openssl rand -base64 20 | sed -re 's/(.....)/&-/g' -e 's/[/,+,=]/A/g' | awk '{print tolower($0)}'`**
  - **`uuidgen | tr '[:upper:]' '[:lower:]'`**

---

<br>

##### ✦ 🐾 Create new 🟢S3 Bucket:

- 📌 e.g., <mark>**On 🔵CloudShell**</mark> (AWS managed network)

```bash-session
### 🚨Define variables (replace with real values)
# export AWS_DEFAULT_REGION=us-west-2
# export SAM_CLI_SOURCE_BUCKET=_Something_


### Create the bucket
# \aws s3api create-bucket --bucket ${SAM_CLI_SOURCE_BUCKET:-NULL} --region ${AWS_DEFAULT_REGION:-NULL} --create-bucket-configuration LocationConstraint=${AWS_DEFAULT_REGION:-NULL}
```

>```json
>{
>    "Location": "http://_Something_.s3.amazonaws.com/"
>}
>```

<br>

##### ✦ 🐾 Apply a 📄Secure Bucket Policy:

- **Explanation**
  - ✅ 1. `“Sid”: “AllowSAMAccess”`
    - This allows **AWS SAM (CloudFormation)** to access the bucket during deployments
  - ✅ 2. `“Sid”: "AllowAccountToAvoidLockout"`
    - This allows the **AWS account** to access the bucket. [⚠️ **Lockout of S3 Bucket** <i class="fa fa-external-link-square-alt"></i>](https://repost.aws/articles/ARZE8eiGwITGKoAOJmHMm-kg/s3-bucket-lockout-recovery-using-iam-root-sessions)
  - 🚫 3. `“Sid”: "ExplicitDenyPublicAccess"`
    - This is an <mark>**explicit deny**</mark>, which takes precedence over any other “allow” policy.
    - Although AWS now blocks public access **by default**, this policy ensures that **even if someone changes the bucket settings**, public access is still denied. 
    - Condition → Enforces **TLS (https)** for secure data transfer.

<br>

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSAMAccess",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "cloudformation.amazonaws.com",
          "serverlessrepo.amazonaws.com"
        ]
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceAccount": "${ACCOUNT_ID}"
        }
      }
    },
    {
      "Sid": "AllowAccountToAvoidLockout",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${ACCOUNT_ID}:root"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}",
        "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}/*"
      ]
    },
    {
      "Sid": "ExplicitDenyPublicAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "*",
      "Resource": [
        "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}",
        "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

<br>

- Create a bucket-policy.json file:
  - Put it to the 🟢**S3 Bucket** for 🟠**AWS SAM**

```bash-session
### 🚨Define variables
# export ACCOUNT_ID=`\aws sts get-caller-identity --query Account --output text`

### Apply the bucket policy (It needs "ACCOUNT_ID" and "SAM_CLI_SOURCE_BUCKET" to create policy file with template file)
# envsubst < bucket-policy-template.json > bucket-policy.json
# \aws s3api put-bucket-policy --bucket ${SAM_CLI_SOURCE_BUCKET} --policy file://bucket-policy.json
# unset ACCOUNT_ID
```

<br>

##### ✦ 🐾 Verify creation:

- (Optional) Check the result:

```bash-session
# pwsh -C "aws s3api get-bucket-policy --bucket ${SAM_CLI_SOURCE_BUCKET} --output text | ConvertFrom-Json | select -expandProperty Statement"

# aws s3api get-bucket-encryption --bucket ${SAM_CLI_SOURCE_BUCKET}

    # If not, Enable default encryption (AES256)
    aws s3api put-bucket-encryption --bucket ${SAM_CLI_SOURCE_BUCKET} --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

<details>

<summary>📖An example of output</summary>

>```ps1
>Sid       : ExplicitDenyPublicAccess
>Effect    : Deny
>Principal : *
>Action    : *
>Resource  : {arn:aws:s3:::sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat, 
>            arn:aws:s3:::sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat/*}
>Condition : @{Bool=}
>
>Sid       : AllowSAMAccess
>Effect    : Allow
>Principal : @{Service=cloudformation.amazonaws.com}
>Action    : {s3:PutObject, s3:GetObject}
>Resource  : arn:aws:s3:::sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat/*
>Condition : @{StringEquals=}
>
>Sid       : AllowAccountOwnerToAvoidLockout
>Effect    : Allow
>Principal : @{AWS=System.Object[]}
>Action    : s3:*
>Resource  : {arn:aws:s3:::sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat, 
>            arn:aws:s3:::sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat/*}
>```

>```json
>{
>    "ServerSideEncryptionConfiguration": {
>        "Rules": [
>            {
>                "ApplyServerSideEncryptionByDefault": {
>                    "SSEAlgorithm": "AES256"
>                },
>                "BucketKeyEnabled": false
>            }
>        ]
>    }
>}
>```

</details>

---

<br>

#### ✰ 🐾 C. **Create new 🟠ECR Private Repo and Register new container image**

<br>

---

<br>

##### ✦ 🐾 Create new 🟠ECR Private Repository:

<br>

📌 e.g., <mark>**On 🔵CloudShell**</mark> (AWS managed network)

<br>

- **Repository Structure**
  - 💡 Amazon 🟠**ECR** is NOT a **blob storage model** like 🟢**S3**, it does not treat / as a hierarchical directory or prefix.

```bash
### Not this,
debut/
├── baseImages
├── tools
└── apps

### This!
Repository Name: debut/tools
Repository Name: debut/baseImages
Repository Name: debut/apps
```

<br>

```bash-session
### 🚨Define variables
# APPS_REPO_NAME=debut/apps/caddy-tls ; APPS_CERT_REPO_NAME=debut/apps/cert-injector ; SCAN_TOOL_REPO_NAME=debut/tools/trivy

### Create 🟠ECR Private Repo for Your Custom Images
# for repo in "${APPS_REPO_NAME}" "${APPS_CERT_REPO_NAME}" "${SCAN_TOOL_REPO_NAME}" ; do \aws ecr create-repository --repository-name ${repo} ; done

### Put lifecycle policy
# for repo in "${APPS_REPO_NAME}" "${APPS_CERT_REPO_NAME}" "${SCAN_TOOL_REPO_NAME}" ; do \aws ecr put-lifecycle-policy --repository-name ${repo} --lifecycle-policy-text file://lifecycle-policy.json ; done

### Enable Basic image-scanning
# for repo in "${APPS_REPO_NAME}" "${APPS_CERT_REPO_NAME}" "${SCAN_TOOL_REPO_NAME}" ; do \aws ecr put-image-scanning-configuration --repository-name ${repo} --image-scanning-configuration scanOnPush=true ; done

  (Option: Only for cross-acct.) # \aws ecr put-registry-policy --policy-text file://registry_policy.json
```

<details>

<summary>📖An example of output</summary>

>```console
>{
>    "repository": {
>        "repositoryArn": "arn:aws:ecr:us-west-2:041920240204:repository/debut/apps",
>        "registryId": "041920240204",
>        "repositoryName": "debut/apps",
>        "repositoryUri": "041920240204.dkr.ecr.us-west-2.amazonaws.com/debut/apps",
>        "createdAt": "2025-05-28T14:47:53.801000+00:00",
>        "imageTagMutability": "MUTABLE",
>        "imageScanningConfiguration": {
>            "scanOnPush": false
>        },
>        "encryptionConfiguration": {
>            "encryptionType": "AES256"
>        }
>    }
>}
>:
>
>
>{
>    "registryId": "041920240204",
>    "repositoryName": "debut/apps",
>    "lifecyclePolicyText": "{\"rules\":[{\"rulePriority\":1,\"description\":\"Retain only the last 5 pushed images\",\"selection\":>{\"tagStatus\":\"any\",\"countType\":\"imageCountMoreThan\",\"countNumber\":5},\"action\":{\"type\":\"expire\"}}]}"
>}
>:
>
>
>{
>    "registryId": "041920240204",
>    "repositoryName": "debut/apps",
>    "imageScanningConfiguration": {
>        "scanOnPush": true
>    }
>}
>:
>```

</details>

<br>

🤨 **Quick Summary Cheat Sheet of image lifecycle**

| Task | Command |
|---|---|
| Apply lifecycle policy | aws ecr put-lifecycle-policy --repository-name ${APPS_REPO_NAME:-NULL} --lifecycle-policy-text file://lifecycle-policy.json |
| Check current policy | aws ecr get-lifecycle-policy --repository-name ${APPS_REPO_NAME:-NULL} |
| Start a dry-run preview | aws ecr start-lifecycle-policy-preview --repository-name ${APPS_REPO_NAME:-NULL} |
| Get preview results | aws ecr get-lifecycle-policy-preview --repository-name ${APPS_REPO_NAME:-NULL} |

<br>

- (Optional) Check the result:

```bash-session
# pwsh -C "\$data = aws ecr describe-repositories | ConvertFrom-Json ; \$data.repositories"
# pwsh -C "\$data = aws ecr describe-repositories | ConvertFrom-Json ; \$data.repositories.repositoryName"
```

>```ps1
>repositoryArn              : arn:aws:ecr:us-west-2:041920240204:repository/debut/apps
>registryId                 : 041920240204
>repositoryName             : debut/apps
>repositoryUri              : 041920240204.dkr.ecr.us-west-2.amazonaws.com/debut/apps
>createdAt                  : 5/28/2025 2:47:53 PM
>imageTagMutability         : MUTABLE
>imageScanningConfiguration : @{scanOnPush=True}
>encryptionConfiguration    : @{encryptionType=AES256}
>:
>
>
>debut/tools/trivy
>debut/apps/caddy-tls
>debut/apps/cert-injector
>```

---

<br>

##### ✦ 🐾 Register Application images:

<br>

```bash-session
### 🚨Define variables
# export AWS_DEFAULT_REGION=us-west-2
# ACCOUNT_ID=`\aws sts get-caller-identity | jq -r .Account`
# REPOSITORY="${ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${APPS_REPO_NAME}" ; echo ${REPOSITORY}
# APP_BLUE_NAME="${APPS_REPO_NAME:-NULL}:arm64-v1.0.0" ; APP_GREEN_NAME="${APPS_REPO_NAME:-NULL}:arm64-v2.0.0" ; APP_CERT_NAME="${APPS_CERT_REPO_NAME:-NULL}:arm64" ; SCAN_TOOL_IMAGE="${SCAN_TOOL_REPO_NAME:-NULL}:0.62.1"

### Load pre-build application images
# mkdir -p /tmp/123RGB && tar xzf all-in-one.tar.gz -C /tmp/123RGB && for val in `ls -1 /tmp/123RGB/*tar` ; do echo ${val} | xargs -tp -I % sh -c 'docker load < %' ; done

  ### (Option): 🛡Check the image architecture
  # docker images --format '{{.Repository}}:{{.Tag}} -> {{.ID}}' --filter reference='caddy-tls:*' --filter reference='apps/cert-injector*'
  # docker images --filter reference='caddy-tls:*' --filter reference='apps/cert-injector*' --format '{{.Repository}}:{{.Tag}} {{.ID}}' | while read ref id ; do arch=$(docker inspect --format '{{.Architecture}}' "$id") ; echo "$ref -> $arch" ; done

### Replace tags
# docker tag caddy-tls:arm64-v1.0.0 ${APP_BLUE_NAME} && docker rmi caddy-tls:arm64-v1.0.0
# docker tag caddy-tls:arm64-v2.0.0 ${APP_GREEN_NAME} && docker rmi caddy-tls:arm64-v2.0.0
# docker tag apps/cert-injector:arm64 ${APP_CERT_NAME} && docker rmi apps/cert-injector:arm64
```

>```console
>sh -c 'docker load < /tmp/123RGB/caddy_tls_amd64-v1.0.0.tar'?...y
>5e00b62e22a2: Loading layer [==================================================>]  41.93MB/41.93MB
>f7daf12848ed: Loading layer [==================================================>]  3.072kB/3.072kB
>f93f48a4d428: Loading layer [==================================================>]  3.072kB/3.072kB
>dcd676464c48: Loading layer [==================================================>]  4.608kB/4.608kB
>Loaded image: caddy-tls:amd64-v1.0.0
>:
>
>
>apps/cert-injector:arm64 -> 5b9ca6a35e1c
>apps/cert-injector:amd64 -> d1e6dc1ac246
>caddy-tls:amd64-v2.0.0 -> fbd50a79e9e8
>caddy-tls:arm64-v2.0.0 -> 98416beb0a20
>caddy-tls:amd64-v1.0.0 -> 9385db98ef8e
>caddy-tls:arm64-v1.0.0 -> 3b8eb383f91e
>
>apps/cert-injector:arm64 -> arm64
>apps/cert-injector:amd64 -> amd64
>caddy-tls:amd64-v2.0.0 -> amd64
>caddy-tls:arm64-v2.0.0 -> arm64
>caddy-tls:amd64-v1.0.0 -> amd64
>caddy-tls:arm64-v1.0.0 -> arm64
>
>
>Untagged: caddy-tls:arm64-v1.0.0
>Untagged: caddy-tls:arm64-v2.0.0
>Untagged: apps/cert-injector:arm64
>```

<br>

|💡Image Scanning: Reactive vs. Proactive |
|---|

| Tool/Method |Timing |Behavior |Use Case |
|---|---|---|---|
| **Trivy** (Manual or CI/CD) | <mark>**Proactive**</mark> | You scan before pushing or deploying | Prevent vulnerabilities from ever entering 🟠**ECR** or production |
| 🟠**ECR Scan on Push**<br>(by 🔴**Amazon Inspector**💰) | **Reactive** | Scans after image is pushed | Detect missed vulnerabilities and alert early |

- 🔁 Both are important:
  - Trivy helps you fail fast in pipelines.
  - Scan on Push gives you early warnings post-push (like safety net).

<br>

```bash-session
### Get latest trivy from Docker Hub
# docker pull aquasec/trivy:latest ; VERSION=`docker inspect aquasec/trivy:latest | jq '.[].Config.Labels."org.opencontainers.image.version"' -r` ; echo ${VERSION:-NULL}
# docker tag aquasec/trivy:latest aquasec/trivy:${VERSION} ; docker rmi aquasec/trivy:latest ; docker images aquasec/trivy:${VERSION}
# SCAN_TOOL_IMAGE="aquasec/trivy:${VERSION}" ; echo ${SCAN_TOOL_IMAGE}

### 🛡[Image Vulnerability Scan]: Security scan the application images
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "${SCAN_TOOL_IMAGE}" image --exit-code 1 --severity HIGH,CRITICAL "${APP_BLUE_NAME}"
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "${SCAN_TOOL_IMAGE}" image --exit-code 1 --severity HIGH,CRITICAL "${APP_GREEN_NAME}"
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "${SCAN_TOOL_IMAGE}" image --exit-code 1 --severity HIGH,CRITICAL "${APP_CERT_NAME}"


### 🛡[SBOM Generation (CycloneDX)]: Generating SBOM for built image
# mkdir ./output
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ./output:/output "${SCAN_TOOL_IMAGE}" image --format cyclonedx --output /output/sbom.cdx_blue.json "${APP_BLUE_NAME}"
# docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ./output:/output "${SCAN_TOOL_IMAGE}" image --format cyclonedx --output sbom.cdx_blue.json "${APP_GREEN_NAME}"


  ###(Option): ✅ Check the Performance
  # docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive caddy-tls-arm64:v1.0.0
```

>```console
>2025-04-05T17:14:34Z    INFO    [vulndb] Need to update DB
>2025-04-05T17:14:34Z    INFO    [vulndb] Downloading vulnerability DB...
>2025-04-05T17:14:34Z    INFO    [vulndb] Downloading artifact...        repo="mirror.gcr.io/aquasec/trivy-db:2"
>:
>Report Summary
>
>┌────────────────────────────────────────┬──────────┬─────────────────┬─────────┐
>│                 Target                 │   Type   │ Vulnerabilities │ Secrets │
>├────────────────────────────────────────┼──────────┼─────────────────┼─────────┤
>│ caddy                                  │ gobinary │        0        │    -    │
>├────────────────────────────────────────┼──────────┼─────────────────┼─────────┤
>│ /etc/caddy/certs/child_private_key.pem │   text   │        -        │    1    │
>└────────────────────────────────────────┴──────────┴─────────────────┴─────────┘
>Legend:
>- '-': Not scanned
>- '0': Clean (no security findings detected)
>/etc/caddy/certs/child_private_key.pem (secrets)
>================================================
>Total: 1 (HIGH: 1, CRITICAL: 0)
>
>HIGH: AsymmetricPrivateKey (private-key)
>════════════════════════════════════════
>Asymmetric Private Key
>────────────────────────────────────────
> /etc/caddy/certs/child_private_key.pem:1 (added by 'COPY child_private_key.pem /etc/caddy/ce')
>────────────────────────────────────────
>   1 [ -----BEGIN PRIVATE KEY-----*************************************-----END PRIVATE KEY
>   2   
>────────────────────────────────────────
>
>
>2025-04-05T17:18:00Z    INFO    "--format cyclonedx" disables security scanning. Specify "--scanners vuln" explicitly if you want to include vulnerabilities in the "cyclonedx" report.
>2025-04-05T17:18:02Z    INFO    Number of language-specific files       num=1
>```

>![image](../../assets/ImageDive.jpg?featherlight=false)

🙄 Why this is Good (Security & Performance):
- ✅ **No attack surface** — no /bin/sh, no package manager, no shell, no busybox.
- ✅ **Minimal footprint** — 39MB image, super fast startup time.
- ✅ **High image efficiency** — no wasted layers or space.
- ✅ **Perfect for ECS Fargate / Cloud Native deployments** — reduces CVE risk.

<br>

```bash-session
### Push the SAFE application images to the 🟠ECR
# docker push "${APP_BLUE_IMAGE}" && docker push "${APP_GREEN_IMAGE}"
# docker logout ${ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com
# unset ACCOUNT_ID
```

---

<br>

### 2️⃣ **[Deploy foundational infrastructure]**

<br>

---

<br>

#### ✰ 🐾 A. **🔴SSM Parameter Store settings**

<br>

This template stores critical infrastructure parameters in **AWS Systems Manager** (🔴**SSM**) - **Parameter Store**, allowing easy access for other components for avoiding hardcoded values.

<br>

- 📌 Required Parameters in yaml:
- `StageName`: Test
- `ACMCertificateArn` : **<i>arn:aws:acm:us-west-2:<ACCOUNT-ID>:certificate/xxxx</i>**
- `VPCName`: TS-VPC
- `AvailabilityZones`: us-west-2a,us-west-2b,us-west-2c,us-west-2d 
- `ALBName` : TS-ALB
- `ALBPrefix` : alb-access-logs
- `ALBS3BucketName` : **<i>alb-access-logs-xxx</i>**
- `ECRRepoName`: debut
- `ECSClusterName` : TS-ECS-Cluster
- `ECSServiceBlueName` : TS-ECS-Service-Blue
- `ECSServiceGreenName` : TS-ECS-Service-Green
- `ECSContainerBlueName` : TTPD-caddy-tls-blue
- `ECSContainerGreenName` : TTPD-caddy-tls-green
- `ECSContainerImageBlueName` : **Unknown** (Update 300 takeout coffees later)
- `ECSContainerImageGreenName` : **Unknown** (Update 300 takeout coffees later)
- `ECSTaskDefinitionBlueName` : TS-11
- `ECSTaskDefinitionGreenName` : TS-11
  - [💡Tips: **General purpose 🟢S3 Bucket naming rules**](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html#create-bucket-name-guid) 
      - Useful commands for generate globally unique identifiers
      - **`openssl rand -base64 20 | sed -re 's/(.....)/&-/g' -e 's/[/,+,=]/A/g' | awk '{print tolower($0)}'`**
      - **`uuidgen | tr '[:upper:]' '[:lower:]'`**

<br>

- `--config-env` (Environment name): <i>SSM-PS</i>

> 💡 **Note:**
> Oh, you've lost previous outputs of the ACM?🥲  
>```bash-session
># aws acm list-certificates --includes 'keyTypes=[EC_prime256v1]'
>```

```bash-session
### 🚨Define variables (replace with your values)
# export STACK_NAME=SSM-PS ; export ACM_CRT_ARN=arn:aws:acm:xxx
# export ALBLOGS_S3_BUCKET_NAME=alb-access-logs-xxx

### Deploy SSM P.S.
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml \
 --parameter-overrides ParameterKey=ACMCertificateArn,ParameterValue=${ACM_CRT_ARN:-NULL} \
 ParameterKey=ALBS3BucketName,ParameterValue=${ALBLOGS_S3_BUCKET_NAME:-NULL} \
 ParameterKey=ECRRepoName,ParameterValue=${APPS_REPO_NAME:-NULL} \
 ParameterKey=ECSContainerImageBlueName,ParameterValue=${IMAGE_NAME_BLUE:-NULL} \
 ParameterKey=ECSContainerImageGreenName,ParameterValue=${IMAGE_NAME_GREEN:-NULL} 
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

<details>

<summary>📖An example of output</summary>

>```console
>Saved parameters to config file 'samconfig.toml' under environment 'SSM-PS': {'template_file':                                                 
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/ECSCluster/SSM.yaml', 's3_bucket':                        
>'sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat', 'capabilities': ('CAPABILITY_IAM',), 'confirm_changeset': True, 'stack_name':     
>'SSM-PS', 's3_prefix': 'SSM-PS', 'parameter_overrides': {'ACMCertificateArn':                                                                  
>'arn:aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877', 'VPCID': 'vpc-04eb144fbc892a756', 'PublicSubnet1':      
>'subnet-0bd101d568021aa90', 'PublicSubnet2': 'subnet-0d810cc3927a7c34f', 'PrivateSubnet1': 'subnet-0d7f2ab2debcfaec5', 'PrivateSubnet2':            
>'subnet-041e2332ed5212e8d'}}                                                                                                                        
>
>        Deploying with following values
>        ===============================
>        Stack name                   : SSM-PS
>        Region                       : us-west-2
>        Confirm changeset            : True
>        Disable rollback             : False
>        Deployment s3 bucket         : sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat
>        Capabilities                 : null
>        Parameter overrides          : {"ACMCertificateArn": "arn:aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877"}
>        Signing Profiles             : {}
>:
>Successfully created/updated stack - SSM-PS in us-west-2
>```

</details>

---

<br>

##### ✦ 🐾 (Optional): Verify creation:

<br>

```bash-session
# PATH_NAME=/ECSCluster

### Only Parameter name
# pwsh -C "(aws ssm get-parameters-by-path --path ${PATH_NAME} --recursive --with-decryption | ConvertFrom-Json).Parameters | ft Name"

### Details
# pwsh -C "(aws ssm get-parameters-by-path --path ${PATH_NAME} --recursive --with-decryption | ConvertFrom-Json).Parameters"
```

<details>

<summary>📖An example of output</summary>

>```ps1
>Name
>----
>/ECSCluster/ACMCertificateArn
>/ECSCluster/ALB/ALBName
>/ECSCluster/ALB/ALBPrefix
>/ECSCluster/ALB/S3BucketName
>/ECSCluster/ECR/RepoName
>/ECSCluster/ECS/Blue/ContainerImageName
>/ECSCluster/ECS/Blue/ServiceName
>/ECSCluster/ECS/Blue/TaskDefinitionName
>/ECSCluster/ECS/ClusterName
>/ECSCluster/StageName
>/ECSCluster/ECS/Blue/ContainerName
>/ECSCluster/ECS/Green/ContainerImageName
>/ECSCluster/ECS/Green/ContainerName
>/ECSCluster/ECS/Green/ServiceName
>/ECSCluster/ECS/Green/TaskDefinitionName
>/ECSCluster/VPC/AvailabilityZones
>/ECSCluster/VPC/VPCName
>
>
>Name             : /ECSCluster/ACMCertificateArn
>ARN              : aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877
>Type             : String
>LastModifiedDate : 2/24/2025 5:11:57 AM
>Description      : SSL/TLS certificate ARN for ALB.
>Version          : 1
>Tier             : Standard
>Policies         : {}
>DataType         : text
>```

</details>

<br>

- Get all values

```bash-session
### Swich to pwsh from zsh or bash
# pwsh


### 🚨Define variables
PS1> $parameterNames = (aws ssm get-parameters-by-path --path /ECSCluster/ --recursive --with-decryption | ConvertFrom-Json).Parameters | Select-Object -ExpandProperty Name

PS1> $batchSize = 10
for ($i = 0; $i -lt $parameterNames.Count; $i += $batchSize) {
    $batch = $parameterNames[$i..($i + $batchSize - 1)]
    Write-Host "`nFetching parameters: $($batch -join ', ')"
    
    # Fetch parameter values for each batch
    if ($batch.Count -gt 0) {
        $parameterValues = aws ssm get-parameters --names $batch --with-decryption | ConvertFrom-Json
        $parameterValues.Parameters | Select-Object Name, Value | Sort-Object Name
    }
}

PS1> Ctrl+D
```

<details>

<summary>📖An example of output</summary>

>```ps1
>Name                                    Value
>----                                    -----
>/ECSCluster/ACMCertificateArn           aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877
>/ECSCluster/ALB/ALBName                 TS-ALB
>/ECSCluster/ALB/ALBPrefix               alb-access-logs
>/ECSCluster/ALB/S3BucketName            alb-access-logs-6rhsm-ih2cr-zsexs-thgir-syawla-tfiws-rolyat
>/ECSCluster/ECR/RepoName                debut
>/ECSCluster/ECS/Blue/ContainerImageName Unknown-ECS-Container-ImageName-300-takeout-coffees-later
>/ECSCluster/ECS/Blue/ServiceName        TS-ECS-Service-Blue
>/ECSCluster/ECS/Blue/TaskDefinitionName TS-11
>/ECSCluster/ECS/ClusterName             TS-ECS-Cluster
>/ECSCluster/StageName                   Test
>/ECSCluster/ECS/Blue/ContainerName      TTPD-caddy-tls-blue
>/ECSCluster/ECS/Green/ContainerImageNa… Unknown-ECS-Container-ImageName-300-takeout-coffees-later
>/ECSCluster/ECS/Green/ContainerName     TTPD-caddy-tls-green
>/ECSCluster/ECS/Green/ServiceName       TS-ECS-Service-Green
>/ECSCluster/ECS/Green/TaskDefinitionNa… TS-11
>/ECSCluster/VPC/AvailabilityZones       us-west-2a,us-west-2b,us-west-2c,us-west-2d
>/ECSCluster/VPC/VPCName                 TS-VPC
>```

</details>

---

<br>

#### ✰ 🐾 B. **Deploy Basic 🟣VPC**

<br>

This template creates a **basic 🟣VPC** with:
  - Public and private **subnets**
  - An **Internet Gateway**
  - **Routing tables**
  - **Network ACLs** for security

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>└── VPC (CIDR: 10.0.0.0/16, DNS Support & Hostnames enabled)
>    ├── InternetGateway
>    │   └── VPCGatewayAttachment -> ../../VPC
>    ├── NetworkAcl-Private
>    │   ├── NetworkAclEntry
>    │   └── SubnetNetworkAclAssociation -> ../Subnet-Private
>    ├── NetworkAcl-Public
>    │   ├── NetworkAclEntry
>    │   └── SubnetNetworkAclAssociation -> ../Subnet-Public
>    ├── RouteTable-Public
>    │   ├── Route -> ../InternetGateway
>    │   └── SubnetRouteTableAssociation -> ../Subnet-Public
>    ├── Subnet-Private (CIDR: 10.0.3.0/24|10.0.4.0/24)
>    └── Subnet-Public  (CIDR: 10.0.1.0/24|10.0.2.0/24 Public IP enabled)
>```

</details>

---

<br>

##### ✦ 🐾 Create 🟣Networking:

- `--config-env` (Environment name): <i>Basic-VPC</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=Basic-VPC

### Deploy Basic Network components and update SSM P.S.
### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_AUTO_EXPAND --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=Basic-VPC
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_AUTO_EXPAND --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

<details>

<summary>📖An example of output</summary>

>```console
>Saved parameters to config file 'samconfig.toml' under environment 'Basic-VPC': {'template_file':                                              
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/ECSCluster/VPC.yaml', 's3_bucket':                        
>'sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat', 'confirm_changeset': True, 'stack_name': 'Basic-VPC'}                                                                                                                                   
>
>        Deploying with following values
>        ===============================
>        Stack name                   : Basic-VPC
>        Region                       : us-west-2
>        Confirm changeset            : True
>        Disable rollback             : False
>        Deployment s3 bucket         : sam-artifacts-i8dcn-ptyw8-kejkz-thgir-syawla-tfiws-rolyat
>        Capabilities                 : ["CAPABILITY_AUTO_EXPAND"]
>        Parameter overrides          : {}
>        Signing Profiles             : {}
>
>Initiating deployment
>=====================
>        Uploading to Basic-VPC/4c19afjdlfjfldsa93aff1klflds58d6.template  1278 / 1278  (100.00%)
>Waiting for changeset to be created..
>
>CloudFormation stack changeset
>-----------------------------------------------------------------------------------------------------------------------------------------
>Operation                          LogicalResourceId                  ResourceType                       Replacement                      
>-----------------------------------------------------------------------------------------------------------------------------------------
>+ Add                              SSMParameterStoreUpdateVPC         AWS::CloudFormation::Stack         N/A                              
>+ Add                              VPC                                AWS::CloudFormation::Stack         N/A                              
>-----------------------------------------------------------------------------------------------------------------------------------------
>:
>Previewing CloudFormation changeset before deployment
>======================================================
>Deploy this changeset? [y/N]: y
>:
>Outputs                                                                                                                                    
>--------------------------------------------------------------------------------------------------------------------------------------------
>Key                 InternetGatewayID                                                                                                     
>Description         The ID of the Internet Gateway                                                                                        
>Value               igw-04ca4950fc38b30fc 
>
>Key                 PrivateSubnetIDs                                                                                                      
>Description         List of Private Subnet IDs                                                                                            
>Value               subnet-0bd101d568021aa90,subnet-060c837df9ac244cb
>
>Key                 PublicSubnetIDs                                                                                                       
>Description         List of Public Subnet IDs                                                                                             
>Value               subnet-0098718f155b9053c,subnet-00e3e29cde16a260b                                                                     
>
>Key                 VPCID                                                                                                                  
>Description         The ID of the created VPC                                                                                              
>Value               vpc-04eb144fbc892a756                                                                                                  
>
>Key                 PublicRouteTableIDs                                                                                                   
>Description         List of Public Route table IDs                                                                                        
>Value               rtb-060fjdslfjsdlbds2,rtb-540sfsiooadsl1sd3                                                                           
>
>Key                 PublicNetworkAcl                                                                                                       
>Description         The IDs of the Public Network ACL                                                                                      
>Value               acl-0186d0fc904c83db5                                                                                                  
>
>Key                 PrivateNetworkAcl                                                                                                      
>Description         The IDs of the Private Network ACL                                                                                     
>Value               acl-0a5eb352accf9cfcb   
>Key                 SSMParamPrivateSubnet1                                                                                                
>Description         SSM Parameter storing the first private subnet ID. (Updated)                                                          
>Value               /ECSCluster/VPC/PrivateSubnet1                                                                                    
>
>Key                 SSMParamPrivateSubnet2                                                                                                
>Description         SSM Parameter storing the second private subnet ID. (Updated)                                                         
>Value               /ECSCluster/VPC/PrivateSubnet2                                                                                    
>
>Key                 SSMParamVPC                                                                                                           
>Description         SSM Parameter storing the VPC ID. (Updated)                                                                           
>Value               /ECSCluster/VPC/VPCID  
>
>Key                 SSMParamPublicSubnet2                                                                                                 
>Description         SSM Parameter storing the second public subnet ID. (Updated)                                                          
>Value               /ECSCluster/VPC/PublicSubnet2                                                                                     
>
>Key                 SSMParamPublicSubnet1                                                                                                 
>Description         SSM Parameter storing the first public subnet ID. (Updated)                                                           
>Value               /ECSCluster/VPC/PublicSubnet1   
>--------------------------------------------------------------------------------------------------------------------------------------------
>
>Successfully created/updated stack - Basic-VPC in us-west-2
>```

</details>

<br>

##### ✦ 🐾 Update the values of 🔴SSM Parameter Store:

- Update the values of the following parameters
  - `/ECSCluster/VPC/VPCID`
  - `/ECSCluster/VPC/PublicSubnet1`
  - `/ECSCluster/VPC/PublicSubnet2`
  - `/ECSCluster/VPC/PrivateSubnet1`
  - `/ECSCluster/VPC/PrivateSubnet2`

> 💡 **Note:**
> Oh, you've lost previous outputs?🥲  
>```bash-session
># sam list stack-outputs --stack-name Basic-VPC
>```

<br>

🙃 Actually, **There are two way to update.**

1. 🔵**AWLCLI**

```bash-session
### 🚨Define variables (replace with your values and repeat to Subnets.)
# PRAM_NAME=/ECSCluster/VPC/VPCID VALUE=vpc-04eb144fbc892a756

# aws ssm put-parameter --name ${PRAM_NAME:-NULL} --value ${VALUE:-NULL} --type "String" --overwrite
```

or

2. 🟠**AWS SAM**

```bash-session
### 🚨Define variables
# export STACK_NAME=SSM-PS

# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --confirm-changeset --save-params --config-env ${STACK_NAME:-NULL} \
  --parameter-overrides ParameterKey=VPCID,ParameterValue=vpc-xxx \
  ParameterKey=PublicSubnet1,ParameterValue=subnet-xxx \
  ParameterKey=PublicSubnet2,ParameterValue=subnet-xxx \
  ParameterKey=PrivateSubnet1,ParameterValue=subnet-xxx \
  ParameterKey=PrivateSubnet2,ParameterValue=subnet-xxx
```

<br>

##### ✦ 🐾 Verify creation:

- Check the result:

```bash-session
### Swich to pwsh from zsh or bash
# pwsh


### 🚨Define variables
PS1> $parameterNames = (aws ssm get-parameters-by-path --path /ECSCluster/VPC --recursive --with-decryption | ConvertFrom-Json).Parameters | Select-Object -ExpandProperty Name

PS1> $batchSize = 10
for ($i = 0; $i -lt $parameterNames.Count; $i += $batchSize) {
    $batch = $parameterNames[$i..($i + $batchSize - 1)]
    Write-Host "`nFetching parameters: $($batch -join ', ')"
    
    # Fetch parameter values for each batch
    if ($batch.Count -gt 0) {
        $parameterValues = aws ssm get-parameters --names $batch --with-decryption | ConvertFrom-Json
        $parameterValues.Parameters | Select-Object Name, Value
    }
}

PS1> Ctrl+D
```

>```ps1 {hl_lines=["6-10"]}
>Fetching parameters: /ECSCluster/VPC/AvailabilityZones, /ECSCluster/VPC/NatGatewayID, /ECSCluster/VPC/PrivateSubnet1, /ECSCluster/VPC/PrivateSubnet2, /ECSCluster/VPC/PublicSubnet1, /ECSCluster/VPC/PublicSubnet2, /ECSCluster/VPC/VPCID, /ECSCluster/VPC/VPCName
>
>Name                                  Value
>----                                  -----
>/ECSCluster/VPC/AvailabilityZones us-west-2a,us-west-2b,us-west-2c,us-west-2d
>/ECSCluster/VPC/PrivateSubnet1    subnet-0d7f2ab2debcfaec5
>/ECSCluster/VPC/PrivateSubnet2    subnet-041e2332ed5212e8d
>/ECSCluster/VPC/PublicSubnet1     subnet-0bd101d568021aa90
>/ECSCluster/VPC/PublicSubnet2     subnet-060c837df9ac244cb
>/ECSCluster/VPC/VPCID             vpc-04eb144fbc892a756
>/ECSCluster/VPC/VPCName           TS-VPC
>```

---

<br>

#### ✰ 🐾 C. **Deploy 🟣VPC-Extras💰**

<br>

This template adds a 🟣**NAT Gateway**, `security groups`, and optional 🟣**VPC endpoints** for 🟠**ECS services**.  
It also adds 🟣**VPC Flowlogs**.  

> 💡 **Note:**  
> 🙄 Why Do We Need a 🟣**NAT Gateway** for `Private` 🟠**ECS**?  
  >>When an image is pulled using a pull through cache rule for **the first time**, if you've configured Amazon ECR to use an interface VPC endpoint using AWS PrivateLink then <u>**you need to create a public subnet in the same VPC, with a NAT gateway,**</u> and then route all outbound traffic to the internet from their private subnet to the NAT gateway in order for the pull to work. **Subsequent image pulls don't require this.** [^2]

<br>

>⚠️ Cost Warning: [^3]  
>🟣**NAT Gateway** and 🟣**VPC Endpoints** incur hourly and data transfer costs. To prevent unexpected charges, delete the stack when not in use.  
>🟣**VPC Flow Logs** incur charges based on the amount of logged data.  

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy(✅) something like this,
>├── LogGroup-VPCFlowLogs ✅
>└── VPC (CIDR: 10.0.0.0/16, DNS Support & Hostnames enabled)
>    ├── EIP ✅
>    ├── FlowLog ✅
>    │   ├── LogGroup-VPCFlowLogs -> ../../LogGroup-VPCFlowLogs
>    │   └── Role-VPCFlowLogs -> ../../Role-VPCFlowLogs
>    ├── InternetGateway
>    │   └── VPCGatewayAttachment -> ../../VPC
>    ├── NetworkAcl-Private
>    │   ├── NetworkAclEntry
>    │   └── SubnetNetworkAclAssociation -> ../Subnet-Private
>    ├── NetworkAcl-Public
>    │   ├── NetworkAclEntry
>    │   └── SubnetNetworkAclAssociation -> ../Subnet-Public
>    ├── RouteTable-Private ✅
>    │   ├── Route -> ../Subnet-Public/NatGateway ✅
>    │   └── SubnetRouteTableAssociation -> ../Subnet-Private ✅
>    ├── RouteTable-Public
>    │   ├── Route -> ../InternetGateway
>    │   └── SubnetRouteTableAssociation -> ../Subnet-Public
>    ├── SecurityGroup-Private-General ✅
>    ├── Subnet-Private (CIDR: 10.0.3.0/24|10.0.4.0/24)
>    │   ├── VPCEndpoint-ECR-API -> ../../SecurityGroup-Private-VPCEndpoints ✅
>    │   ├── VPCEndpoint-ECR-CWLogs -> ../../SecurityGroup-Private-VPCEndpoints ✅
>    │   ├── VPCEndpoint-ECR-DKR -> ../../SecurityGroup-Private-VPCEndpoints ✅
>    │   └── VPCEndpoint-S3 ✅
>    └── Subnet-Public  (CIDR: 10.0.1.0/24|10.0.2.0/24 Public IP enabled)
>        └── NatGateway -> ../EIP ✅
>```

</details>

<br>

- `--config-env` (Environment name): <i>VPC-Extras-Gen2Endpoint</i> / <i>VPC-Extras-Flowlogs</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=VPC-Extras-Gen2Endpoint

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=VPC-Extras-Gen2Endpoint
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

<details>

<summary>📖An example of output</summary>

>```console
>Saved parameters to config file 'samconfig.toml' under environment 'VPC-Extras-Gen2Endpoint': {'template_file':                                
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/ECSCluster/VPC_Extras_Gen2Endpoint.yaml', 's3_bucket':    
>'sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat', 'confirm_changeset': True, 'stack_name': 'VPC-Extras-Gen2Endpoint', 's3_prefix':  
>'VPC-Extras-Gen2Endpoint'}                                                                                                                     
>
>        Deploying with following values
>        ===============================
>        Stack name                   : VPC-Extras-Gen2Endpoint
>        Region                       : us-west-2
>        Confirm changeset            : True
>        Disable rollback             : False
>        Deployment s3 bucket         : sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat
>        Capabilities                 : null
>        Parameter overrides          : {}
>        Signing Profiles             : {}
>:
>Successfully created/updated stack - VPC-Extras-Gen2Endpoint in us-west-2
>```

</details>

<br>

```bash-session
### 🚨Define variables
# export STACK_NAME=VPC-Extras-Flowlogs

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=VPC-Extras-Flowlogs
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

---

<br>

#### ✰ 🐾 D. **Deploy 🟠Lambda for ALB Logs Forwarding & 🟢S3**

<br>

This step sets up ALB logs forwarding to CloudWatch Logs

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>├── Lambda
>│   └── Function
>│       ├── LogGroup-ALB -> ../../LogGroup-ALB
>│       └── LogGroup-Lambda -> ../../LogGroup-Lambda
>├── LogGroup-ALB
>├── LogGroup-Lambda
>├── Role-ECSTask
>├── S3-ALB
>│   └── S3Trigger -> ../Lambda
>```

</details>

<br>

- `--config-env` (Environment name): <i>ALB-LogsForwarder</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ALB-LogsForwarder

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=ALB-LogsForwarder
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

<details>

<summary>📖An example of output</summary>

>```console
>CloudFormation stack changeset
>-----------------------------------------------------------------------------------------------------------------------------------------
>Operation                          LogicalResourceId                  ResourceType                       Replacement                      
>-----------------------------------------------------------------------------------------------------------------------------------------
>+ Add                              ALBLogGroup                        AWS::Logs::LogGroup                N/A                              
>+ Add                              ALBLogS3BucketPolicy               AWS::S3::BucketPolicy              N/A                              
>+ Add                              ALBLogS3Bucket                     AWS::S3::Bucket                    N/A                              
>+ Add                              ALBLogsForwarderFunctionS3Trigge   AWS::Lambda::Permission            N/A                              
>                                   rPermission                                                                                            
>+ Add                              ALBLogsForwarderFunction           AWS::Lambda::Function              N/A                              
>+ Add                              ALBLogsForwarderLogGroup           AWS::Logs::LogGroup                N/A                              
>+ Add                              ALBLogsForwarderRole               AWS::IAM::Role                     N/A                              
>-----------------------------------------------------------------------------------------------------------------------------------------
>:
>CloudFormation outputs from deployed stack
>-------------------------------------------------------------------------------------------------------------------------------------------
>Outputs                                                                                                                                   
>-------------------------------------------------------------------------------------------------------------------------------------------
>Key                 ALBLogsForwarderLogGroupName                                                                                          
>Description         Name of the CloudWatch Log Group for Lambda.                                                                          
>Value               /Lambda/ECSCluster/Test/ALBLogsForwarder                                                                          
>
>Key                 ALBCostWarning                                                                                                        
>Description         ?? Warning: ALB is a paid service with hourly and LCU-based charges. ? Be cautious!                                   
>Value               ALB is running and may generate costs. Delete the stack when not in use.                                              
>
>Key                 ALBLogsForwarderARN                                                                                                   
>Description         ARN of the Lambda function.                                                                                           
>Value               ALB-LogsForwarder-ALBLogsForwarderFunction-DfISYHkC7eoM                                                               
>
>Key                 ALBLogGroupName                                                                                                       
>Description         Name of the CloudWatch Log Group for ALB logs.                                                                        
>Value               /ALB/ECSCluster/Test/AccessLogs/TS-ALB                                                                            
>-------------------------------------------------------------------------------------------------------------------------------------------
>
>Successfully created/updated stack - ALB-LogsForwarder in us-west-2
>```

</details>

---

<br>

#### ✰ 🐾 E. **Deploy Internal 🔴ALB💰**

<br>

>⚠️ Cost Warning: [^3]  
>The Application Load Balancer (🔴**ALB**) is a paid service and incurs hourly and LCU-based charges.

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>└── VPC
>    ├── SecurityGroup-Private-ALB -> SecurityGroup-Private-HTTPS
>    ├── SecurityGroup-Private-HTTPS
>    ├── SecurityGroup-Private-VPCEndpoints
>    ├── Subnet-Private
>    │   ├── LoadBalancer
>    │   │   ├── Listener -> ../../../ACM-ALB
>    │   │   ├── S3-ALB -> ../../../S3-ALB
>    │   │   ├── SecurityGroup-Private-ALB -> ../../SecurityGroup-Private-ALB
>    │   │   └── TargetGroup
>```

</details>

<br>

- `--config-env` (Environment name): <i>ALB</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ALB

### Deploy ALB components and update SSM P.S.
### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_AUTO_EXPAND --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=ALB
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

<br>

#### ✰ 🐾 F. **Deploy 🟠ECS Cluster**

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>├── ECS-Cluster
>└── VPC
>    └── SecurityGroup-Private-Fargate -> SecurityGroup-Private-ALB
>```

</details>

>⚠️ Cost Warning: [^3]  
>The 🟠**Fargate** is a paid service and incurs hourly and vCPU and storage based charges.

- `--config-env` (Environment name): <i>ECS</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ECS

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME}.yaml


  ### After the second
  # export STACK_NAME=ECS
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL} 
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```



---

<br>

### 3️⃣ **[Deploy initial 🟠ECS Service for 'Blue' environment]**

<br>

---

<br>

#### ✰ 🐾 A. **Deploy 🟠ECS Service & 🟠Fargate💰**

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>├── LogGroup-ECS
>├── Role-ECSTask
>└── VPC
>    ├── Subnet-Private
>    │   ├── ECS-Service
>    │   │   ├── ECS-Cluster -> ../../../ECS-Cluster
>    │   │   ├── SecurityGroup-Private-Fargate -> ../../SecurityGroup-Private-Fargate
>    │   │   └── TaskDefinition
>    │   │       ├── LogGroup-ECS -> ../../../../LogGroup-ECS
>    │   │       └── Role-ECSTask -> ../../../../Role-ECSTask
>```

</details>

<br>

>⚠️ Cost Warning: [^3]  
>The 🟠**Fargate** is a paid service and incurs hourly and vCPU and storage based charges.

- `--config-env` (Environment name): <i>ECSCluster</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ECSCluster

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME}.yaml


  ### After the second
  # export STACK_NAME=ECSCluster
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL} 
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

---

<br>

#### ✰ 🐾 B. **Deploy 🔴Application Auto Scaling**

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>├── ApplicationAutoScaling
>│   ├── ScalableTarget
>│   │   ├── ECS-Service -> ../../VPC/Subnet-Private/ECS-Service
>│   │   └── Role-AutoScaling -> ../../Role-AutoScaling
>│   └── ScalingPolicy -> ScalableTarget
>├── Role-AutoScaling
>```

</details>

<br>

- `--config-env` (Environment name): <i>ECS-AppAutoScaling</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ECS-AppAutoScaling

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME##*-}.yaml


  ### After the second
  # export STACK_NAME=ECS-AppAutoScaling
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

---

<br>

### ☻ **[Test the Connection]**

<br>

📌 <mark>**On 🔵CloudShell in `Private` Subnet**</mark>

|🙄How to create CloudShell within Private Subnet?||
|---|---|
|![image](../../assets/FargateCluster-CS1.jpg)|![image](../../assets/FargateCluster-CS2.jpg)|

<br>

```bash-session
### Upload Root certificate
# cat > certificate.crt
Ctrl+D

# ALB_DNS=TSALB-545957675.us-west-2.elb.amazonaws.com
# curl -vk --cacert certificate.crt https://${ALB_DNS:-NULL} -H "Host: Betty.swiftie.com"
# curl -vk --cacert certificate.crt https://${ALB_DNS:-NULL} -H "Host: James.swiftie.com"
```

- Copy and paste this to send a request

```console
GET / HTTP/1.1
Host: Betty.swiftie.com
Connection: close
```

---

<br>

### 4️⃣ (Option): **[Deploy initial 🟠ECS Service for 'Green' environment]**

<br>

---

### 🚮 **Clean it up**

<br>

```bash-session
### 🔴Application Auto Scaling
# sam delete --config-env ECS-AppAutoScaling


### 🟠ECSCluster💰 and 🟠ECR
# sam delete --config-env ECSCluster
# aws ecr delete-repository --repository-name debut


### 🔴ALB💰
# sam delete --config-env ALB-Internal


### 🟠Lambda and 🟢S3
# PRAM_NAME=/ECSCluster/ALB/S3BucketName
# S3_BUCKET_NAME=`aws ssm get-parameter --name ${PRAM_NAME:-NULL} | jq -r '.Parameter.Value'`

### Delete all objects, including Versions and Delete-markers
# \aws s3api delete-objects --bucket ${S3_BUCKET_NAME} \
--delete "$(\aws s3api list-object-versions --bucket ${S3_BUCKET_NAME} \
--query='{Objects: Versions[].{Key:Key,VersionId:VersionId}}' --output json)" 2>/dev/null

  ### Also delete Delete-markers (if any)
  # \aws s3api delete-objects --bucket ${S3_BUCKET_NAME} \
  --delete "$(\aws s3api list-object-versions --bucket ${S3_BUCKET_NAME} \
  --query='{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' --output json)" 2>/dev/null

### Confirm Bucket is Empty
# aws s3api list-object-versions --bucket ${S3_BUCKET_NAME}

# aws s3 rb s3://${S3_BUCKET_NAME:-NULL} --force
# sam delete --config-env ALB-LogsForwarder


### 🟣VPC-Extras💰
# sam delete --config-env VPC-Extras-Gen2Endpoint
# sam delete --config-env VPC-Extras-Flowlogs


### 🔴SSM ParameterStore
# sam delete --config-env SSM-PS


### 🟣VPC
# sam delete --config-env Basic-VPC
```

>```console
>        Enter stack name you want to delete: Basic-VPC
>        Are you sure you want to delete the stack Basic-VPC in the region us-west-2 ? [y/N]: y
>        - Deleting Cloudformation stack Basic-VPC
>
>Deleted successfully
>
>SAM CLI update available (1.134.0); (1.131.0 installed)
>To download: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
>```

>```console
>{
>    "Deleted": [
>        {
>            "Key": "Basic-VPC/58b5a0cf8ff24b3c7a895642d642a825.template",
>            "VersionId": "null"
>        }
>    ]
>}
>
>
>{
>    "RequestCharged": null,
>    "Prefix": ""
>}
>
>
>remove_bucket: sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat
>```

---

<br>

#### ✰ (Option): Check Actual Costs🫣

<br>

- $START_DATE: <i>2025-01-18</i>
- $END_DATE: <i>2025-01-19</i>

```bash-session
# START_DATE=`date -u -v-1d +%Y-%m-%d` ; END_DATE=`date -u +%Y-%m-%d` ; echo ${START_DATE} "-" ${END_DATE}
# aws ce get-cost-and-usage --time-period Start=${START_DATE:-NULL},End=${END_DATE:-NULL} --granularity DAILY --metrics UnblendedCost
```

>```console {hl_lines=[12]}
>2025-01-18 - 2025-01-19
>
>{
>   "ResultsByTime": [
>       {
>           "TimePeriod": {
>               "Start": "2025-01-18",
>               "End": "2025-01-19"
>           },
>           "Total": {
>               "UnblendedCost": {
>                   "Amount": "0.698262188",
>                   "Unit": "USD"
>               }
>           },
>           "Groups": [],
>           "Estimated": true
>       }
>   ],
>   "DimensionValueAttributes": []
>}
>```

---

---

<br>

> 💡 **Note:**

[^1]: The Security piller of AWS Well-Architected Framework
- AWS Cloud Foundations
  - [**SEC01-BP01**: Separate workloads using accounts](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_multi_accounts.html)
    - ![image](https://d1.awsstatic.com/product-marketing/organizations/Product-Page-Diagram_Organizational-Foundational-Units.d709f66bf4c45ed1af01360f3d39adecc1a99fb4.png)
    - [**Establishing your best practice AWS environment**](https://aws.amazon.com/organizations/getting-started/best-practices/)
  - [**SEC04-BP01**: Configure service and application logging](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_app_service_logging.html)
    - [**CloudWatch cross-account observability**](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)
    - [**Guidance for Observability on AWS**](https://aws.amazon.com/solutions/guidance/observability-on-aws/)
      - [PDF](https://d1.awsstatic.com/solutions/guidance/architecture-diagrams/observability-on-aws.pdf)
- Security foundations
  - [**SEC01-BP06**: Automate deployment of standard security controls](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_automate_security_controls.html)

[^2]: [**Considerations for Amazon ECR VPC endpoints**](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html#ecr-vpc-endpoint-considerations)

[^3]: - The Pricing list😣 
- [**NAT gateways Pricing**](https://aws.amazon.com/vpc/pricing/)
- [**PrivateLink pricing Pricing**](https://aws.amazon.com/privatelink/pricing/)
- [**Elastic Load Balancing pricing**](https://aws.amazon.com/elasticloadbalancing/pricing/)
- [**VPC Flow Logs Pricing**](https://aws.amazon.com/cloudwatch/pricing/)
- [**AWS Fargate Pricing**](https://aws.amazon.com/fargate/pricing/)

---
