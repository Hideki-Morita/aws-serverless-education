# Cloud-Native Application architecture: Fargate Cluster

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

- [Cloud-Native Application architecture: Fargate Cluster](#cloud-native-application-architecture-fargate-cluster)
  - [🪩 Table of Contents](#-table-of-contents)
  - [🪩 Architecture Overview](#-architecture-overview)
    - [☻ About Deployment strategy](#-about-deployment-strategy)
    - [☻ Deployment Order](#-deployment-order)
  - [🪩 Deployment Steps](#-deployment-steps)
    - [☻ Requirements](#-requirements)
      - [✰ Python modules](#-python-modules)
      - [✰ AWS PoLP Permissions for a workforce as a deployer](#-aws-polp-permissions-for-a-workforce-as-a-deployer)
    - [0️⃣ Create a Virtual Environment (Recommended)](#0️⃣-create-a-virtual-environment-recommended)
    - [1️⃣ 🔴ACM - Upload SSL/TLS Certificates](#1️⃣-acm---upload-ssltls-certificates)
    - [2️⃣ Deploy 🟣VPC](#2️⃣-deploy-vpc)
      - [✰ 🐾 A. Create Secure 🟢S3 Bucket for 🟠SAM Artifacts](#--a-create-secure-s3-bucket-for-sam-artifacts)
        - [✦ 🐾 **Create new 🟢S3 Bucket:**](#--create-new-s3-bucket)
        - [✦ 🐾 **Apply a 📄Secure Bucket Policy**](#--apply-a-secure-bucket-policy)
        - [✦ 🐾 **Verify creation:**](#--verify-creation)
      - [✰ 🐾 B. 🔴SSM Parameter Store settings](#--b-ssm-parameter-store-settings)
      - [✰ 🐾 C. Basic 🟣VPC Setup](#--c-basic-vpc-setup)
        - [✦ 🐾 **Create 🟣Networking:**](#--create-networking)
        - [✦ 🐾 **Update the values of 🔴SSM Parameter Store:**](#--update-the-values-of-ssm-parameter-store)
        - [✦ 🐾 **Verify creation:**](#--verify-creation-1)
      - [✰ 🐾 D. 🟣VPC-Extras💰](#--d-vpc-extras)
    - [3️⃣ Deploy 🟠Lambda for ALB Logs Forwarding \& 🟢S3](#3️⃣-deploy-lambda-for-alb-logs-forwarding--s3)
    - [4️⃣ Deploy Internal 🔴ALB💰](#4️⃣-deploy-internal-alb)
    - [5️⃣ Deploy 🟠ECR \& 🟠ECS Fargate Cluster💰](#5️⃣-deploy-ecr--ecs-fargate-cluster)
      - [✰ 🐾 A. **Create new 🟠ECR Private Repo:**](#--a-create-new-ecr-private-repo)
      - [✰ 🐾 B. **Deploy 🟠Fargate Cluster:**](#--b-deploy-fargate-cluster)
    - [6️⃣ Deploy 🔴Application Auto Scaling](#6️⃣-deploy-application-auto-scaling)
    - [☻ Test the Connection](#-test-the-connection)
    - [🚮 Clean it up](#-clean-it-up)
      - [✰ (Option) Check Actual Costs🫣](#-option-check-actual-costs)

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
- 🟠**Fargate cluster** and 🔴**Application Auto Scaling** for serverless container workloads
- <i>Manual operations</i>:
  - 🔴**AWS Certificate Manager** (ACM) for provide End-to-End encrypt transit 

|High-level overview|
|---|
|![image](../../assets/FargateCluster-HighLevel-Overview.jpg)|

|Details|
|---|
|![image](../../assets/FargateCluster-Overview.jpg?)|

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

| yaml | purpose |
|---|---|
| 1. **SSM_PS.yaml** | Stores important parameters (e.g., VPC ID, ALB settings) in SSM Parameter Store. |
| 2. **Basic_VPC.yaml** | Creates the VPC, subnets, and routing. |
| 3. **VPC_Extras_Gen2Endpoint.yaml** | Adds additional networking resources like NAT Gateway and VPC Endpoints. |
| 4. **VPC_Extras_Flowlogs.yaml** | Enables VPC Flow Logs for monitoring network traffic. |
| 5. **ALB_LogsForwarder.yaml** | Sets up forwarding of ALB access logs to S3 or another logging solution. |
| 6. **ALB_Internal.yaml** | Deploys the internal ALB for routing requests within the VPC. |
| 7. **FargateCluster.yaml** | Provisions the ECS Fargate cluster for running serverless containerized applications. |
| 8. **AppAutoScaling.yaml** | Configures application auto-scaling policies for Fargate tasks. |

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

### 0️⃣ Create a Virtual Environment (Recommended)

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
# cd serverless-education/Serverless_Architecture/FargateCluster
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
>(awsvenv) user@hostname:~/aws-serverless-education/Serverless_Architecture/FargateCluster$ 
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
>You should consider upgrading via the '/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/FargateCluster/awsvenv/bin/>python3 -m pip install --upgrade pip' command.
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
>You should consider upgrading via the '/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/FargateCluster/awsvenv/bin/>python3 -m pip install --upgrade pip' command
>```

---

<br>

### 1️⃣ 🔴ACM - Upload SSL/TLS Certificates

<br>

- 📌 Example Files:
  - **Root Certificate**: <i>certificate.crt</i>  
  - **Child Certificate**: <i>child_certificate.crt</i>  
  - **Child Private Key**: <i>child_private_key.pem</i>  

<details>

<summary>📖Summary of Certificates</summary>

- **Key algorithm**
  - **EC** with **P-256 curve**

- **certificate.crt (Root Certificate)**
  - issuer=CN=mastermind.swiftie.com
  - subject=CN=mastermind.swiftie.com
  - notBefore=Feb 15 10:52:02 2025 GMT
  - notAfter=Feb 28 10:52:02 2029 GMT

- **child_certificate.crt (Child Certificate)**
  - issuer=CN=mastermind.swiftie.com
  - subject=CN=*.swiftie.com
  - notBefore=Feb 15 11:15:00 2025 GMT
  - notAfter=Feb 14 11:15:00 2029 GMT
  - X509v3 Subject Alternative Name: 
  -     DNS:*.swiftie.com, DNS:Betty.swiftie.com, DNS:James.swiftie.com, DNS:Inez.swiftie.com, DNS:swiftie.com

</details>

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

### 2️⃣ Deploy 🟣VPC

---

<br>

#### ✰ 🐾 A. Create Secure 🟢S3 Bucket for 🟠SAM Artifacts

<br>

> 🙄Why create a custom 🟢**S3 Bucket** for 🟠**AWS SAM**?

By default, 🟠**AWS SAM** creates an 🟢**S3 Bucket** with a <u>predictable name</u>, like **aws-sam-cli-managed-default-samclisourcebucket**-xxxxxxxx.  

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

##### ✦ 🐾 **Create new 🟢S3 Bucket:**

- 📌 e.g., <mark>**On 🔵CloudShell**</mark> (AWS managed network)

```bash-session
### Define variables (replace with your values)
# export SAM_CLI_SOURCE_BUCKET=_Something_
# export AWS_DEFAULT_REGION=us-west-2


### Create the bucket
# aws s3api create-bucket --bucket ${SAM_CLI_SOURCE_BUCKET:-NULL} --region ${AWS_DEFAULT_REGION:-NULL} --create-bucket-configuration LocationConstraint=${AWS_DEFAULT_REGION:-NULL}
```

>```json
>{
>    "Location": "http://_Something_.s3.amazonaws.com/"
>}
>```

<br>

##### ✦ 🐾 **Apply a 📄Secure Bucket Policy**

- **Explanation**
  - ✅ 1. `“Sid”: “AllowSAMAccess”`
    - This allows **AWS SAM (CloudFormation)** to access the bucket during deployments
  - ✅ 2. `“Sid”: AllowAccountOwnerToAvoidLockout`
    - This allows the **AWS account owner (root user)** to access the bucket. [⚠️ **Lockout of S3 Bucket** <i class="fa fa-external-link-square-alt"></i>](https://repost.aws/articles/ARZE8eiGwITGKoAOJmHMm-kg/s3-bucket-lockout-recovery-using-iam-root-sessions)
  - 🚫 3. `“Sid”: “DenyPublicAccess”`
    - This is an <mark>**explicit deny**</mark>, which takes precedence over any other “allow” policy.
    - Although AWS now blocks public access **by default**, this policy ensures that **even if someone changes the bucket settings**, public access is still denied. 
    - Condition → Enforces **TLS (https)** for secure data transfer.
<br>

  ```json {hl_lines=["10-11",17,"27-29"]}
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
          "s3:GetObject"
        ],
        "Resource": "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}/*",
        "Condition": {
          "StringEquals": {
            "AWS:SourceAccount": "${ACCOUNT_ID}"
          }
        }
      },
      {
        "Sid": "AllowAccountOwnerToAvoidLockout",
        "Effect": "Allow",
        "Principal": {
          "AWS": [
            "arn:aws:iam::${ACCOUNT_ID}:root",
            "${ASSUMED_ROLE_ARN}",
            "arn:aws:iam::${ACCOUNT_ID}:role/aws-reserved/sso.amazonaws.com/us-west-2/${ASSUMED_ROLE_NAME}"
          ]
        },
        "Action": "s3:*",
        "Resource": [
          "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}",
          "arn:aws:s3:::${SAM_CLI_SOURCE_BUCKET}/*"
        ]
      },
      {
        "Sid": "ExplicitDenyPublicAccess",
        "Principal": "*",
        "Effect": "Deny",
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
### 🚨Define variables (replace with real values)
# export ACCOUNT_ID=`\aws sts get-caller-identity --query Account --output text`
# export ASSUMED_ROLE_ARN=`\aws sts get-caller-identity --query Arn --output text`
# export ASSUMED_ROLE_NAME=`echo ${ASSUMED_ROLE_ARN} | cut -f 2 -d "/"`

### Apply the bucket policy
# envsubst < bucket-policy-template.json > bucket-policy.json
# aws s3api put-bucket-policy --bucket ${SAM_CLI_SOURCE_BUCKET} --policy file://bucket-policy.json
# unset ACCOUNT_ID ASSUMED_ROLE_ARN ASSUMED_ROLE_NAME
```

<br>

##### ✦ 🐾 **Verify creation:**

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

#### ✰ 🐾 B. 🔴SSM Parameter Store settings

<br>

This template stores critical infrastructure parameters in **AWS Systems Manager** (🔴**SSM**) - **Parameter Store**, allowing easy access for other components for avoiding hardcoded values.

<br>

- 📌 Required Parameters in yaml:
  - `ACMCertificateArn` : **<i>arn:aws:acm:us-west-2:<ACCOUNT-ID>:certificate/xxxx</i>**
  - `VPCName`: TS-VPC
  - `VPCID` : **<i>vpc-xxxx</i>**
  - `PrivateSubnet1` : **<i>subnet-xxxa</i>**
  - `PrivateSubnet2` : **<i>subnet-xxxb</i>**
  - `PublicSubnet1` : **<i>subnet-xxxc</i>**
  - `PublicSubnet2` : **<i>subnet-xxxd</i>**
  - `AvailabilityZones`: us-west-2a,us-west-2b,us-west-2c,us-west-2d
  - `NatGatewayID` : **Unknown** (Update later)
  - `ALBSecurityGroupName` : **Unknown** (Update later)
  - `ALBTargetGroupARN` : **Unknown** (Update later)
  - `ALBName` : TS-ALB
  - `ALBS3BucketName` : **Unknown** (Update later)
  - `ALBPrefix` : alb-access-logs
  - `ECSClusterName` : TS-ECS-Cluster
  - `ECSServiceName` : TS-ECS-Service
  - `ECSTaskDefinitionName`: TS-11
  - `ECSContainerName`: TTPD-nginx
  - `ECSContainerImageName`: **Unknown** (Update later)
  - `ECRRepoName`: debut
  - `StageName`: Test
  - [💡Tips: **General purpose 🟢S3 Bucket naming rules**](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html#create-bucket-name-guid) 
      - Useful commands for generate globally unique identifiers
      - **`openssl rand -base64 20 | sed -re 's/(.....)/&-/g' -e 's/[/,+,=]/A/g' | awk '{print tolower($0)}'`**
      - **`uuidgen | tr '[:upper:]' '[:lower:]'`**

<br>

- `--config-env` (Environment name): <i>SSM-PS</i>

> 💡 **Note:**
> Oh, you've lost previous outputs?🥲  
>```bash-session
># aws acm list-certificates --includes 'keyTypes=[EC_prime256v1]'
>```

```bash-session
### 🚨Define variables (replace with your values)
# export STACK_NAME=SSM-PS ; export ACM_CRT_ARN=xxx

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml \
 --parameter-overrides ParameterKey=ACMCertificateArn,ParameterValue=${ACM_CRT_ARN:-NULL}


  ### After the second
  # export STACK_NAME=SSM-PS ; export ACM_CRT_ARN=xxx
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
>Saved parameters to config file 'samconfig.toml' under environment 'SSM-PS': {'template_file':                                                 
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/FargateCluster/SSM.yaml', 's3_bucket':                        
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

<br>

- (Optional) Check the result:

```bash-session
# PATH_NAME=/FargateCluster

### Only name
# pwsh -C "(aws ssm get-parameters-by-path --path ${PATH_NAME} --recursive --with-decryption | ConvertFrom-Json).Parameters | ft Name"

### Details
# pwsh -C "(aws ssm get-parameters-by-path --path ${PATH_NAME} --recursive --with-decryption | ConvertFrom-Json).Parameters"
```

<details>

<summary>📖An example of output</summary>

>```ps1
>Name                                  
>----                                  
>/FargateCluster/ACMCertificateArn     
>/FargateCluster/ALB/ALBName           
>/FargateCluster/ALB/ALBPrefix         
>/FargateCluster/ALB/S3BucketName      
>/FargateCluster/ALB/SecurityGroupName 
>/FargateCluster/ALB/TargetGroupARN    
>/FargateCluster/ECR/RepoName          
>/FargateCluster/ECS/ServiceName       
>/FargateCluster/ECS/TaskDefinitionName
>/FargateCluster/StageName             
>/FargateCluster/ECS/ClusterName       
>/FargateCluster/ECS/ContainerImageName
>/FargateCluster/ECS/ContainerName     
>/FargateCluster/VPC/AvailabilityZones 
>/FargateCluster/VPC/NatGatewayID      
>/FargateCluster/VPC/PrivateSubnet1    
>/FargateCluster/VPC/PrivateSubnet2    
>/FargateCluster/VPC/PublicSubnet1     
>/FargateCluster/VPC/PublicSubnet2     
>/FargateCluster/VPC/VPCName           
>
>
>Name             : /FargateCluster/ACMCertificateArn
>ARN              : arn:arn:aws:acm:us-west-2:041920240204:certificate/ctfiws-3337-4cbf-bedf-rolyatd1a877
>Type             : String
>LastModifiedDate : 2/24/2025 5:11:57 AM
>Description      : SSL/TLS certificate ARN for ALB.
>Version          : 1
>Tier             : Standard
>Policies         : {}
>DataType         : text
>```

</details>

---

<br>

#### ✰ 🐾 C. Basic 🟣VPC Setup

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

##### ✦ 🐾 **Create 🟣Networking:**

- `--config-env` (Environment name): <i>Basic-VPC</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=Basic-VPC

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=Basic-VPC
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
>Saved parameters to config file 'samconfig.toml' under environment 'Basic-VPC': {'template_file':                                              
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/FargateCluster/VPC.yaml', 's3_bucket':                        
>'sam-artifacts-fm7rp-oloif-egci9-exami-sirqh-roa-thgir-syawla-tfiws-rolyat', 'confirm_changeset': True, 'stack_name': 'Basic-VPC'}                                                                                                                                   
>
>        Deploying with following values
>        ===============================
>        Stack name                   : Basic-VPC
>        Region                       : us-west-2
>        Confirm changeset            : True
>        Disable rollback             : False
>        Deployment s3 bucket         : sam-artifacts-i8dcn-ptyw8-kejkz-thgir-syawla-tfiws-rolyat
>        Capabilities                 : null
>        Parameter overrides          : {}
>        Signing Profiles             : {}
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
>Key                 PrivateSubnetID2                                                                                                       
>Description         The ID of the private subnet2                                                                                          
>Value               subnet-041e2332ed5212e8d                                                                                               
>
>Key                 PrivateSubnetID1                                                                                                       
>Description         The ID of the private subnet1                                                                                          
>Value               subnet-0d7f2ab2debcfaec5                                                                                               
>
>Key                 PublicSubnetID2                                                                                                        
>Description         The ID of the public subnet2                                                                                           
>Value               subnet-060c837df9ac244cb                                                                                               
>
>Key                 PublicSubnetID1                                                                                                        
>Description         The ID of the public subnet1                                                                                           
>Value               subnet-0bd101d568021aa90                                                                                               
>
>Key                 VPCID                                                                                                                  
>Description         The ID of the created VPC                                                                                              
>Value               vpc-04eb144fbc892a756                                                                                                  
>
>Key                 PublicNetworkAcl                                                                                                       
>Description         The IDs of the Public Network ACL                                                                                      
>Value               acl-0186d0fc904c83db5                                                                                                  
>
>Key                 PrivateNetworkAcl                                                                                                      
>Description         The IDs of the Private Network ACL                                                                                     
>Value               acl-0a5eb352accf9cfcb                                                                                                  
>--------------------------------------------------------------------------------------------------------------------------------------------
>
>Successfully created/updated stack - Basic-VPC in us-west-2
>SAM CLI update available (1.133.0); (1.131.0 installed)
>```

</details>

<br>

##### ✦ 🐾 **Update the values of 🔴SSM Parameter Store:**

- Update the values of the following parameters
  - `/FargateCluster/VPC/VPCID`
  - `/FargateCluster/VPC/PublicSubnet1`
  - `/FargateCluster/VPC/PublicSubnet2`
  - `/FargateCluster/VPC/PrivateSubnet1`
  - `/FargateCluster/VPC/PrivateSubnet2`

> 💡 **Note:**
> Oh, you've lost previous outputs?🥲  
>```bash-session
># sam list stack-outputs --stack-name Basic-VPC
>```

```bash-session
### 🚨Define variables
# PRAM_NAME=/FargateCluster/VPC/VPCID VALUE=vpc-04eb144fbc892a756

# aws ssm put-parameter --name ${PRAM_NAME:-NULL} --value ${VALUE:-NULL} --type "String" --overwrite
```

<br>

##### ✦ 🐾 **Verify creation:**

- Check the result:

```bash-session
# pwsh

PS1> $parameterNames = (aws ssm get-parameters-by-path --path /FargateCluster/VPC --recursive --with-decryption | ConvertFrom-Json).Parameters | Select-Object -ExpandProperty Name

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

>```ps1 {hl_lines=["7-11"]}
>Fetching parameters: /FargateCluster/VPC/AvailabilityZones, /FargateCluster/VPC/NatGatewayID, /FargateCluster/VPC/PrivateSubnet1, /FargateCluster/VPC/PrivateSubnet2, /FargateCluster/VPC/PublicSubnet1, /FargateCluster/VPC/PublicSubnet2, /FargateCluster/VPC/VPCID, /FargateCluster/VPC/VPCName
>
>Name                                  Value
>----                                  -----
>/FargateCluster/VPC/AvailabilityZones us-west-2a,us-west-2b,us-west-2c,us-west-2d
>/FargateCluster/VPC/NatGatewayID      Unknown-NatGtwyID-300-takeout-coffees-later
>/FargateCluster/VPC/PrivateSubnet1    subnet-0d7f2ab2debcfaec5
>/FargateCluster/VPC/PrivateSubnet2    subnet-041e2332ed5212e8d
>/FargateCluster/VPC/PublicSubnet1     subnet-0bd101d568021aa90
>/FargateCluster/VPC/PublicSubnet2     subnet-060c837df9ac244cb
>/FargateCluster/VPC/VPCID             vpc-04eb144fbc892a756
>/FargateCluster/VPC/VPCName           TS-VPC
>```

---

<br>

#### ✰ 🐾 D. 🟣VPC-Extras💰

<br>

This template adds a 🟣**NAT Gateway**, `security groups`, and optional 🟣**VPC endpoints** for 🟠**ECS services**. It also adds 🟣**VPC Flowlogs**.

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
>'/home/cloudshell-user/Workshop/aws-serverless-education/Serverless_Architecture/FargateCluster/VPC_Extras_Gen2Endpoint.yaml', 's3_bucket':    
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

### 3️⃣ Deploy 🟠Lambda for ALB Logs Forwarding & 🟢S3

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

---

<br>

### 4️⃣ Deploy Internal 🔴ALB💰

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

- `--config-env` (Environment name): <i>ALB-Internal</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=ALB-Internal

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME/-/_}.yaml


  ### After the second
  # export STACK_NAME=ALB-Internal
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL}
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

---

<br>

### 5️⃣ Deploy 🟠ECR & 🟠ECS Fargate Cluster💰

<br>

<details>

<summary>📖Resulting Architecture</summary>

>```console
>### You will deploy something like this,
>├── ECS-Cluster
>├── LogGroup-ECS
>├── Role-ECSTask
>└── VPC
>    ├── SecurityGroup-Private-Fargate -> SecurityGroup-Private-ALB
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

#### ✰ 🐾 A. **Create new 🟠ECR Private Repo:**

<br>

📌 <mark>**On 🔵CloudShell in `Private` Subnet**</mark>

|🙄How to create CloudShell within Private Subnet?||
|---|---|
|![image](../../assets/FargateCluster-CS1.jpg)|![image](../../assets/FargateCluster-CS2.jpg)|

<br>

```bash-session
### 🚨Define variables
# PRAM_NAME=/FargateCluster/ECR/RepoName
# REPO_NAME=`aws ssm get-parameter --name ${PRAM_NAME:-NULL} | jq -r '.Parameter.Value`
# ACCOUNT_ID=`aws sts get-caller-identity | jq -r .Account`

### Create ECR Private Repo for Your Custom Images
# aws ecr create-repository --repository-name ${REPO_NAME:-NULL}

### Pull Nginx from AWS Public ECR
# docker pull --platform=linux/arm64 public.ecr.aws/nginx/nginx:latest

  ### (Option) Check if the image architecture and is available
  # docker inspect --format '{{.Architecture}}' public.ecr.aws/nginx/nginx:latest
  # docker images
```

<details>

<summary>📖An example of output</summary>

>```console
>latest: Pulling from nginx/nginx
>3a4d501ec8d0: Pull complete 
>1529751f7538: Pull complete 
>bbefd32e7dcb: Pull complete 
>47cc26834fb6: Pull complete 
>aba9a01aa562: Pull complete 
>25ef5805725b: Pull complete 
>f6eaf43e06b3: Pull complete 
>Digest: sha256:f62145615fb0af3b134ca97f6df890dab3172eb14ded120ec09fe3ebde90af25
>Status: Downloaded newer image for public.ecr.aws/nginx/nginx:latest
>```

</details>

<br>

```bash-session
### 🚨Define variables
# IMAGE_NAME=${ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/${REPO_NAME}:track5
# PRAM_NAME=/FargateCluster/ECS/ContainerImageName VALUE=${IMAGE_NAME}

### Login to ECR
# aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com

### Tag the Image for AWS ECR
# docker tag public.ecr.aws/nginx/nginx:latest ${IMAGE_NAME:-NULL}

### Push Image to AWS ECR
# docker push ${IMAGE_NAME:-NULL}

### Update SSM Parameter
# aws ssm put-parameter --name ${PRAM_NAME:-NULL} --value ${VALUE:-NULL} --type "String" --overwrite


  ### Option: if you want to update current ECS Cluster, then
  # PRAM_NAME=/FargateCluster/ECS/ClusterName
  # ECSClusterName=`aws ssm get-parameter --name ${PRAM_NAME:-NULL} | jq -r '.Parameter.Value`
  # PRAM_NAME=/FargateCluster/ECS/ServiceName
  # ECSServiceName=`aws ssm get-parameter --name ${PRAM_NAME:-NULL} | jq -r '.Parameter.Value`
  # aws ecs update-service --cluster ${ECSClusterName:-NULL} --service ${ECSServiceName:-NULL} --force-new-deployment

### Logout from AWS ECR
# docker logout ${ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com
```

---

<br>

#### ✰ 🐾 B. **Deploy 🟠Fargate Cluster:**

<br>

>⚠️ Cost Warning: [^3]  
>The 🟠**Fargate** is a paid service and incurs hourly and vCPU and storage based charges.

- `--config-env` (Environment name): <i>FargateCluster</i>

```bash-session
### 🚨Define variables
# export STACK_NAME=FargateCluster

### The first time
# sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --capabilities CAPABILITY_IAM --confirm-changeset --save-params \
 --stack-name ${STACK_NAME:-NULL} --config-env ${STACK_NAME} --s3-prefix ${STACK_NAME} -t ${STACK_NAME}.yaml


  ### After the second
  # export STACK_NAME=FargateCluster
  # sam deploy --s3-bucket ${SAM_CLI_SOURCE_BUCKET} --config-env ${STACK_NAME:-NULL} 
```

```bash-session
Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y
```

---

<br>

### 6️⃣ Deploy 🔴Application Auto Scaling

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

### ☻ Test the Connection

<br>

📌 <mark>**On 🔵CloudShell in `Private` Subnet**</mark>

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

### 🚮 Clean it up

<br>

```bash-session
### 🔴Application Auto Scaling
# sam delete --config-env ECS-AppAutoScaling


### 🟠FargateCluster💰 and 🟠ECR
# sam delete --config-env FargateCluster
# aws ecr delete-repository --repository-name debut


### 🔴ALB💰
# sam delete --config-env ALB-Internal


### 🟠Lambda and 🟢S3
# PRAM_NAME=/FargateCluster/ALB/S3BucketName
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

#### ✰ (Option) Check Actual Costs🫣

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
