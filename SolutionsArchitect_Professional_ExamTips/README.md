## 🪩 Relationship between SAP Exam(SAP-C02) and Well-Architected Framework

<br>

- [AWS-Certified-Solutions-Architect-Professional_Exam-Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf)

<br>

- [**Well-Architected Framework**](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/framework/wellarchitected-framework.pdf#document-revisions)

  - **The Six Pillars Well-Architected Framework**

    - ![image](../assets/AWS_WA_Framework.jpeg)

    - **Immediate Operational Necessity** (`SEC` and `OE` are **non-negotiable** and foundational for immediate operational integrity and excellence.)
      - [Security Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)
      - [Operational Excellence Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/operational-excellence-pillar/wellarchitected-operational-excellence-pillar.pdf)
    - **Balanced Optimization** (`REL`, `PERF`, and `COST` are balanced against each other, often with **trade-offs**, to meet the specific needs and goals of the business.
    )
      - [Performance Efficiency Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/performance-efficiency-pillar/wellarchitected-performance-efficiency-pillar.pdf)
      - [Reliability Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/reliability-pillar/wellarchitected-reliability-pillar.pdf)
      - [Cost Optimization Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/cost-optimization-pillar/wellarchitected-cost-optimization-pillar.pdf)
    - **Strategic Importance** (**Sustainability** is a strategic imperative that influences long-term planning and reflects a commitment to responsible business practices.)
      - [Sustainability Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/sustainability-pillar/wellarchitected-sustainability-pillar.pdf)

---

<br>

Here’s the relational list mapping all domains and task statements from the **AWS Certified Solutions Architect Professional** (SAP-C02) Exam Guide to the <mark>**AWS Well-Architected Framework**</mark> principles:

- [🪩 Relationship between SAP Exam(SAP-C02) and Well-Architected Framework](#-relationship-between-sap-examsap-c02-and-well-architected-framework)
	- [☻ Domain 1: Design Solutions for Organizational Complexity](#-domain-1-design-solutions-for-organizational-complexity)
		- [✰ Task Statement 1.1: Architect _network connectivity_ strategies.](#-task-statement-11-architect-network-connectivity-strategies)
		- [✰ Task Statement 1.2: Prescribe _security_ controls.](#-task-statement-12-prescribe-security-controls)
		- [✰ Task Statement 1.3: Design _reliable_ and resilient architectures.](#-task-statement-13-design-reliable-and-resilient-architectures)
		- [✰ Task Statement 1.4: Design a multi-account AWS environment.](#-task-statement-14-design-a-multi-account-aws-environment)
		- [✰ Task Statement 1.5: Determine cost optimization and visibility strategies.](#-task-statement-15-determine-cost-optimization-and-visibility-strategies)
	- [☻ Domain 2: Design for New Solutions](#-domain-2-design-for-new-solutions)
		- [✰ Task Statement 2.1: Design a deployment strategy to meet business requirements.](#-task-statement-21-design-a-deployment-strategy-to-meet-business-requirements)
		- [✰ Task Statement 2.2: Design a solution to ensure business continuity](#-task-statement-22-design-a-solution-to-ensure-business-continuity)
		- [✰ Task Statement 2.3: Determine security controls based on requirements.](#-task-statement-23-determine-security-controls-based-on-requirements)
	- [☻ Domain 3: Continuous Improvement for Existing Solutions](#-domain-3-continuous-improvement-for-existing-solutions)
		- [✰ Task Statement 3.1: Determine a strategy to improve overall operational excellence.](#-task-statement-31-determine-a-strategy-to-improve-overall-operational-excellence)
		- [✰ Task Statement 3.2: Determine a strategy to improve security.](#-task-statement-32-determine-a-strategy-to-improve-security)

---

<br>

### ☻ Domain 1: Design Solutions for Organizational Complexity

---

<br>

#### ✰ Task Statement 1.1: Architect _network connectivity_ strategies.

- Core BP is **`REL02-BP01`**(High👀): Use highly available **network connectivity** for your workload public endpoints

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Evaluating connectivity options for **multiple VPCs**| - **`REL02-BP03`**: Ensure IP subnet allocation accounts for expansion and availability.|  
|| - - [Building a Scalable and Secure **Multi-VPC** AWS Network Infrastructure](https://docs.aws.amazon.com/pdfs/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/building-scalable-secure-multi-vpc-network-infrastructure.pdf)|
|| - - [Amazon Virtual Private Cloud Connectivity Options](https://d1.awsstatic.com/whitepapers/aws-amazon-vpc-connectivity-options.pdf)|
| 2. Evaluating **connectivity options** for on-premises, co-location, and cloud integration| - **`REL02-BP02`**(High👀): Provision redundant **connectivity between** private networks in the cloud and on-premises environments.|
| 3. **Selecting AWS Regions** and Availability Zones based on **network and latency requirements**| - **`PERF04-BP06`**: **Choose your workload's location** based on **network requirements**|
|| - - `REL10-BP01`(High👀): Deploy the workload to multiple locations| 
|| - - `PERF04-BP02`(High👀): Evaluate available networking features|
|| - - `SUS01-BP01`: **Choose Region** based on both business requirements and sustainability goals|
|| - - `SUS02-BP04`: Optimize geographic placement of workloads based on their **networking requirements**|
| 4. **Troubleshooting traffic** flows by using AWS tools| - **`PERF04-BP07`**: Optimize network configuration based on metrics |
|| - - [AWS re:Invent 2020 – Monitoring and troubleshooting network traffic](https://www.youtube.com/watch?v=Ed09ReWRQXc) |
| 5. Using service endpoints for service integrations | - **`SEC05-BP01`**(High👀): Create network layers|
|| - **`SEC05-BP02`**(High👀): Control traffic flow within your network layers.|

---

<br>

#### ✰ Task Statement 1.2: Prescribe _security_ controls.

- Based on [**Security** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Evaluating **cross-account access** management| - **`SEC03-BP07`**: Analyze public and **cross-account access**|
|| - **`SEC02-BP04`**(High👀): Rely on a centralized identity provider|
|| - **`SEC08-BP04`**(High👀): Enforce access control|
| 2. Integrating with **third-party** identity providers| - **`SEC03-BP09`**: Share resources securely with a **third party**|
| 3. Deploying **encryption** strategies for **data at rest** and **data in transit**|<u>Protecting **data at rest**</u>|
|| - **`SEC08-BP01`**(High👀): Implement secure key management|
|| - **`SEC08-BP02`**(High👀): Enforce **encryption** at rest|
|| - **`SEC08-BР03`**: Automate data at rest protection|
|| - **`SEC08-BP04`**(High👀): Enforce access control|
|| <u>Protecting **data in transit**</u> |
|| - **`SEC09-BP01`**(High👀): Implement secure key and certificate management|
|| - **`SEC09-BP02`**(High👀): Enforce **encryption** in transit|
|| - **`SEC09-BP03`**: Authenticate network communications|
| 4. Developing a strategy for centralized **security event** notifications and auditing| - **`SEC04-BP02`**: Capture logs, findings, and metrics in standardized locations|
|| - **`SEC04-BP03`**: Correlate and enrich **security alerts**|

---

<br>

#### ✰ Task Statement 1.3: Design _reliable_ and resilient architectures.

- Based on [**Reliability** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/reliability-pillar/wellarchitected-reliability-pillar.pdf)

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Designing **disaster recovery** solutions based on **RTO** and **RPO** requirements| <u>Plan for **Disaster Recovery** (DR)</u> |
|| - **`REL13-BP01`**(High👀): Define **recovery objectives** for downtime and data loss|
|| - **`REL13-BP02`**(High👀): Use defined recovery strategies to meet the **recovery objectives**|
|| - **`REL13-BP03`**(High👀): Test disaster recovery implementation to validate the implementation|
|| - **`REL13-BP04`**(High👀): Manage configuration drift at the **DR** site or Region|
| 2. Implementing architectures to **automatically recover** from failure| - **`REL13-BP05`**: **Automate recovery**|
| 3. Developing the optimal architecture by considering **scale-up** and **scale-out** options| - **`REL07-BP01`**(High👀): Use automation when obtaining or **scaling** resources|
|| - - `SUS02-BP01`: Scale workload infrastructure dynamically|
| 4. Designing an effective **backup** and restoration strategy| <u>**Back up** data</u> |
|| - **`REL09-BP01`**(High👀): Identify and **back up** all data that needs to be backed up, or reproduce the datafrom sources|
|| - **`REL09-BP02`**(High👀): Secure and encrypt **backups**|
|| - **`REL09-BP03`**: Perform data **backup** automatically|
|| - **`REL09-BP04`**: Perform periodic recovery of the data to verify **backup** integrity and processes|

---

<br>

#### ✰ Task Statement 1.4: Design a multi-account AWS environment.

- Based on [**Security** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)
  - Core BPs are **`SEC01-BP01`**(High👀) and **`SEC01-BP02`**(High👀):<br> While it applies to all three skills, it’s because  foundational to [**Multi-account strategy**](https://docs.aws.amazon.com/pdfs/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.pdf) and unavoidable.

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Evaluating the most appropriate account structure for organizational requirements| <u>AWS account management and separation</u> |
|| - **`SEC01-BP01`**(High👀): Separate workloads using accounts|
|| - **`SEC01-BP02`**(High👀): Secure account root user and properties|
|| - - **`SEC03-BP03`**: Establish emergency access process|
|| - - **`SEC03-BP05`**: Define permission guardrails for your organization|
|| - - **`SEC03-BP07`**: Analyze public and cross-account access|
|| - - **`SEC08-BP01`**(High👀): Implement secure key management|
|| - - **`OPS05-BP08`**: Use multiple environments|
|| - - **`SEC10-BP03`**: Prepare forensic capabilities|
| 2. Recommending a strategy for **central logging** and **event notifications**| <u>Configure services and resources centrally</u> |
|| - **`SEC04-BP01`**: Configure service and application **logging**|
|| - **`SEC04-BP02`**: Capture logs, findings, and metrics in standardized locations|
|| - - `SEC01-BP01`(High👀): Separate workloads using accounts|
|| - - `SEC06-BP01`(High👀): Perform vulnerability management|
|| - **`OPS08-BP01`**: Analyze workload metrics|
|| - - [**CloudWatch cross-account observability**](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)|
|| - - [**Guidance for Observability on AWS**](https://aws.amazon.com/solutions/guidance/observability-on-aws/)|
|| - - [**Cross account Monitoring with AWS Native services**](https://aws-observability.github.io/observability-best-practices/patterns/multiaccount)|
| 3. Developing a **multi-account** governance model| - **`SEC01-BP01`**(High👀): **Separate workloads** using accounts|
|| - **`SEC10-BP03`**: Prepare forensic capabilities|

---

<br>

#### ✰ Task Statement 1.5: Determine cost optimization and visibility strategies.

- Based on [**Cost Optimization** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/cost-optimization-pillar/wellarchitected-cost-optimization-pillar.pdf)

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. **Monitoring cost** and usage with AWS tools| - **`COST01-BP06`**: **Monitor cost** proactively|
| 2. Developing an effective **tagging strategy** that maps costs to business units| - **`COST03-BP05`**(High👀): Configure billing and cost management tools|
| 3. Understanding how **purchasing options** affect cost and performance| <u>Select **the best pricing model**</u> |
|| - **`COST07-BP01`**(High👀): Perform **pricing model** analysis|
|| - **`COST07-BP02`**: Choose Regions based on cost|
|| - **`COST07-BP03`**: Select third-party agreements with cost-efficient terms|
|| - **`COST07-BP04`**: Implement **pricing models** for all components of this workload|
|| - **`COST07-BP05`**: Perform **pricing model** analysis at the management account level|

---

<br>

### ☻ Domain 2: Design for New Solutions

> [!NOTE]  
> While some knowledge areas **overlap** between Domain 1 and 2, but the **intent** of each task statement provides the differentiation:  
> - Domain 1: Focuses on **design** (e.g., reliability, architecture, and connectivity).  
> - Domain 2: Focuses on **implementation** (e.g., ensuring continuity during disruptions).  

>> e.g.,  
>> Task Statement 1.1: Architect network connectivity strategies.
>> 
>> Knowledge of:  
>> • **AWS Global Infrastructure**  
>> • **AWS networking concepts** (for example, Amazon VPC, AWS Direct Connect, AWS VPN, transitive routing, AWS container services)  
>>   
>> Task Statement 1.3: Design reliable and resilient architectures.  
>>  
>> Knowledge of:  
>> • **Recovery time objectives (RTOs) and recovery point objectives (RPOs)**  
>> • **Disaster recovery** strategies (for example, using AWS Elastic Disaster Recovery, pilot light, warm standby, and multi-site)  
>> • Data backup and restoration  
>>   
>> ---  
>>   
>> Task Statement 2.2: Design a solution to ensure business continuity.  
>>   
>> Knowledge of:  
>> • **AWS Global Infrastructure**  
>> • **AWS networking concepts** (for example, Route 53, routing methods)  
>> • **RTOs and RPOs**  
>> • **Disaster recovery** scenarios (for example, backup and restore, pilot light, warm standby, multi-site)  
>> • **Disaster recovery** solutions on AWS  

---

<br>

#### ✰ Task Statement 2.1: Design a deployment strategy to meet business requirements.

- Core BP is **`REL08-BP04`**: Deploy using immutable infrastructure

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. **Determining an application** or **upgrade** path for new services and features| - **`RELO8-BP04`**: Deploy using immutable infrastructure|
|| - **`SUS06-BP03`**: Keep your workload **up-to-date**|
|| Organization priorities|
|| - **`OPS01-BP01`**(High👀): **Evaluate external customer needs**|
|| - **`OPS01-BP02`**(High👀): **Evaluate internal customer needs**|
|| - **`OPS01-BP04`**(High👀): **Evaluate compliance requirements**|
|| - - `OPS01-BP05`: Evaluate threat landscape|
|| - - `OPS01-BP06`: Evaluate tradeoffs while managing benefits and risks|
| 2. Selecting services to develop **deployment strategies** and implement appropriate **rollback mechanisms**| - **`OPS05-BP04`**: Use build and **deployment** management systems|
|| - **`OPS06-BP03`**: Employ safe **deployment strategies**|
|| - **`REL07-BP01`**(High👀): Use automation when obtaining or scaling resources|
|| - **`REL08-BP04`**: **Deploy** using immutable infrastructure|
|| - **`REL08-BP05`**: **Deploy** changes with automation|
|| - **`OPS06-BP04`**: Automate testing and **rollback**|
| 3. Adopting **managed services** as needed to reduce infrastructure provisioning and **patching** overhead| - **`SEC01-BP05`**: Reduce security management scope|
|| - **`SEC06-BP01`**(High👀): Perform vulnerability management|
|| - **`SUS05-BP03`**: Use managed services|
| 4. Making advanced technologies accessible by delegating **complex development** and deployment tasks to AWS| <u>Mitigate deployment risks</u> |
|| - **`OPS06-BP01`**(High👀): Plan for unsuccessful changes|
|| - **`OPS06-BP02`**(High👀): Test deployments|
|| - **`OPS06-BP03`**: Employ safe **deployment** strategies|
|| - **`OPS06-BP04`**: Automate testing and **rollback**|

---

<br>

#### ✰ Task Statement 2.2: Design a solution to ensure business continuity

<br>

- Based on [**Reliability** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/reliability-pillar/wellarchitected-reliability-pillar.pdf)

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Configuring **disaster recovery** solutions| <u>Plan for **Disaster Recovery** (DR)</u> |
|| - **`REL13-BP01`**(High👀): Define **recovery objectives** for downtime and data loss|
|| - **`REL13-BP02`**(High👀): Use defined recovery strategies to meet the **recovery objectives**|
|| - **`REL13-BP05`**: Automate recovery.|
| 2. Configuring data and database **replication**| - **`REL07-BP01`**(High👀): Use automation when obtaining or scaling resources.|
|| - **`REL09-BP01`**(High👀): Identify and back up all data that needs to be backed up, or reproduce the data from sources.|
| 3. Performing **disaster recovery testing**| - **`REL13-BP03`**(High👀): **Test disaster recovery implementation** to validate the implementation.|
|| - **`REL09-BP04`**: **Perform periodic recovery** of the data to verify backup integrity and processes.|
| 4. Architecting a **backup solution** that is **automated**, is cost-effective, and supports business continuity across multiple Availability Zones or Regions| <u>**Back up data**</u> | |
|| - **`REL09-BP01`**(High👀): Identify and back up all data that needs to be **backed up**, or reproduce the data from sources.|
|| - **`REL09-BP02`**(High👀): Secure and encrypt backups.|
|| - **`REL09-BP03`**: Perform data **backup automatically**.|
| 5. Designing an architecture that provides application and infrastructure availability in **the event of a disruption**| - **`REL11-BP01`**(High👀): Monitor all components of the workload to detect failures.|
|| - **`REL12-BP01`**(High👀): Use playbooks to investigate failures.|
| 6. Using processes and components for **centralized monitoring** to proactively recover from system failures| - **`OPS08-BP01`**: Analyze workload metrics.|
|| - - [**CloudWatch cross-account observability**](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)|
|| - - [**Guidance for Observability on AWS**](https://aws.amazon.com/solutions/guidance/observability-on-aws/)|
|| - - [**Cross account Monitoring with AWS Native services**](https://aws-observability.github.io/observability-best-practices/patterns/multiaccount)|
|| - **`REL13-BP05`**: Automate recovery.|

---

<br>

#### ✰ Task Statement 2.3: Determine security controls based on requirements.

<br>

- Based on [**Security** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Specifying IAM users and IAM roles that adhere to **the principle of least privilege access**| - **`SEC03-BP02`**(High👀): Grant **least privilege access**|
|| - **`SEC03-BP03`**: Establish **emergency access** process|
|| - **`SEC03-BP05`**: **Define permission guardrails** for your organization.|
| 2. Specifying **inbound and outbound** network flows by using **security group** rules and network ACL rules|**`SEC05-BP01`**(High👀): Create network layers.|
|| - **`SEC05-BP02`**(High👀): Control traffic flow within your network layers.|
|| - **`SEC05-BP03`**: Implement inspection-based protection|
| 3. Developing **attack mitigation strategies** for large-scale **web applications**| - **`SEC06-BP01`**(High👀): Perform vulnerability management.|
|| - **`SEC06-BP03`**: Protect networks at all layers.|
| 4. Developing encryption strategies for **data at rest** and **data in transit**|<u>Protecting **data at rest**</u>|
|| - **`SEC08-BP01`**(High👀): Implement secure key management|
|| - **`SEC08-BP02`**(High👀): Enforce **encryption** at rest|
|| - **`SEC08-BР03`**: Automate data at rest protection|
|| <u>Protecting **data in transit**</u> |
|| - **`SEC09-BP01`**(High👀): Implement secure key and certificate management|
|| - **`SEC09-BP02`**(High👀): Enforce **encryption** in transit|
|| - **`SEC09-BP03`**: Authenticate network communications|
| 5. Specifying **service endpoints** for **service integrations**| - **`SEC05-BP01`**(High👀): Create network layers.|
|| - **`SEC05-BP02`**(High👀): Control traffic flow within your network layers.|
|| - **`REL02-BP01`**(High👀): Use highly available network connectivity for your workload public **endpoints**.|
|| - **`REL02-BP02`**(High👀): Provision redundant connectivity between private networks in the cloud and on-premises environments.|
| 6. Developing strategies for **patch management** to remain compliant with organizational standards| - **`SEC06-BP01`**(High👀): Perform **vulnerability management**.|
|| - **`OPS05-BP05`**: Perform **patch management**.|

---

<br>

### ☻ Domain 3: Continuous Improvement for Existing Solutions

<br>

- Based on [Operational Excellence Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/operational-excellence-pillar/wellarchitected-operational-excellence-pillar.pdf)

---

<br>

#### ✰ Task Statement 3.1: Determine a strategy to improve overall operational excellence.

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Determining the most appropriate logging and monitoring strategy| <u>Configure services and resources centrally</u> |
|| - **`SEC04-BP01`**: Configure service and application **logging**|
|| - **`SEC04-BP02`**: Capture logs, findings, and metrics in standardized locations|
|| - - `SEC01-BP01`(High👀): Separate workloads using accounts|
|| - - `SEC06-BP01`(High👀): Perform vulnerability management|
|| - **`OPS08-BP01`**: Analyze workload metrics|
|| - - [**CloudWatch cross-account observability**](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)|
|| - - [**Guidance for Observability on AWS**](https://aws.amazon.com/solutions/guidance/observability-on-aws/)|
|| - - [**Cross account Monitoring with AWS Native services**](https://aws-observability.github.io/observability-best-practices/patterns/multiaccount)|
| 2. Evaluating current deployment processes for **improvement opportunities**| - **`OPS05-BP02`**: Test and validate changes|
|| <u>Learn, share, and **improve**</u> |
|| - **`OPS11-BP01`**(High👀): Have a process for continuous improvement.|
|| - **`OPS11-BP02`**(High👀): Perform post-incident analysis.|
|| - **`OPS11-BP03`**(High👀): Implement feedback loops.|
|| - **`OPS11-BP04`**(High👀): Perform knowledge management.|
|| - - `OPS11-BP07`: Perform operations metrics reviews.|
|| - - `OPS11-BP08`: Document and share lessons learned.|
|| - - `OPS11-BP09`: Allocate time to make improvements.|
| 3. **Prioritizing** opportunities for automation within a solution stack| - **`OPS09-BP03`**: Review operations metrics and **prioritize** improvement.|
|| - **`OPS06-BP02`**: Test deployments.|
| 4. Recommending the appropriate AWS solution to enable configuration management automation| - **`OPS05-BP03`**: Use configuration management systems.|
| 5. Engineering failure scenario activities to support and exercise an understanding of recovery action| - **`OPS07-BP04`**: Use playbooks to investigate issues.|

---

<br>

#### ✰ Task Statement 3.2: Determine a strategy to improve security.

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Evaluating a strategy for the secure management of **secrets** and **credentials**| - **`SEC08-BP01`**: Implement secure key management.|
|| - **`SEC08-BP03`**: Automate data at rest protection.|
|| - **`SEC02-BP02`**: Use **temporary credentials**|
|| - **`SEC02-BP03`**: Store and use **secrets** securely|
|| - **`SEC02-BP05`**: Audit and **rotate credentials** periodically|
| 2. **Auditing** an environment for **least privilege access**| - **`SEC03-BP02`**: Grant **least privilege access**.|
|| - **`SEC05-BP02`**: Control traffic flow within your network layers.|
|| - **`SEC02-BP05`**: **Audit** and rotate credentials periodically|
|| - **`SEC04-BP03`**: Correlate and enrich **security alerts**|
|| - - `SEC03-BP03`: Establish emergency access process.|
| 3. Reviewing implemented solutions to ensure security at **every layer**| - **`SEC03-BP05`**: Define permission guardrails for your organization.|
|| - **`SEC06-BP01`**: Perform vulnerability management.|
|| - **`SEC05-BP03`**: Implement inspection-based protection.|
| 4. Reviewing comprehensive traceability of users and services| - **`SEC04-BP02`**: Capture logs, findings, and metrics in standardized locations.|
|| - **`SEC06-BP02`**: Provision compute from hardened images.|
|| - **`SEC03-BP07`**: Analyze public and cross-account access|
|| 5. Prioritizing automated responses to the detection of vulnerabilities| - **`SEC06-BP01`**: Perform vulnerability management|
|| - **`SEC06-BP05`**: Automate compute protection|
|| - - `SEC06-BP04`: Validate software integrity.|
| 6. Designing and implementing a patch and update process| - **`OPS05-BP05`**: Perform patch management.|
|| - **`SEC06-BP01`**: Perform vulnerability management.|
|| - **`SEC06-BP02`**: Provision compute from hardened images.|
|| - **`SEC01-BP04`**: Stay up to date with security threats and recommendations.|
| 7. Designing and implementing a backup process| - **`REL09-BP01`**: Identify and back up all data that needs to be backed up, or reproduce the data from sources|
|| - **`REL09-BP03`**: Perform data backup automatically|

---