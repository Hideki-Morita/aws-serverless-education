## 🪩 Relationship between SAP Exam(SAP-C02) and Well-Architected Framework

<br>

- [AWS-Certified-Solutions-Architect-Professional_Exam-Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf)

<br>

📌 **The Six Pillars Well-Architected Framework**

![image](../assets/AWS_WA_Framework.jpeg)

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

---

<br>

### ☻ Domain 1: Design Solutions for Organizational Complexity

---

<br>

#### ✰ Task Statement 1.1: Architect _network connectivity_ strategies.

- **`REL02-BP01`**(High👀): Use highly available **network connectivity** for your workload public endpoints

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
|| - - [AWS re:Invent 2020 – Monitoring and troubleshooting network trafic](https://www.youtube.com/watch?v=Ed09ReWRQXc) |
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
| 3. Deploying **encryption** strategies for **data at rest** and **data in transit**|Protecting **data at rest**|
|| - **`SEC08-BP01`**(High👀): Implement secure key management|
|| - **`SEC08-BP02`**(High👀): Enforce **encryption** at rest|
|| - **`SEC08-BР03`**: Automate data at rest protection|
|| - **`SEC08-BP04`**(High👀): Enforce access control|
||Protecting **data in transit**|
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
| 1. Designing **disaster recovery** solutions based on **RTO** and **RPO** requirements|Plan for **Disaster Recovery** (DR)|
|| - **`REL13-BP01`**(High👀): Define **recovery objectives** for downtime and data loss|
|| - **`REL13-BP02`**(High👀): Use defined recovery strategies to meet the **recovery objectives**|
|| - **`REL13-BP03`**(High👀): Test disaster recovery implementation to validate the implementation|
|| - **`REL13-BP04`**(High👀): Manage configuration drift at the **DR** site or Region|
| 2. Implementing architectures to **automatically recover** from failure| - **`REL13-BP05`**: **Automate recovery**|
| 3. Developing the optimal architecture by considering **scale-up** and **scale-out** options| - **`REL07-BP01`**(High👀): Use automation when obtaining or **scaling** resources|
|| - - `SUS02-BP01`: Scale workload infrastructure dynamically|
| 4. Designing an effective **backup** and restoration strategy|**Back up** data|
|| - **`REL09-BP01`**(High👀): Identify and **back up** all data that needs to be backed up, or reproduce the datafrom sources|
|| - **`REL09-BP02`**(High👀): Secure and encrypt **backups**|
|| - **`REL09-BP03`**: Perform data **backup** automatically|
|| - **`REL09-BP04`**: Perform periodic recovery of the data to verify **backup** integrity and processes|

---

<br>

#### ✰ Task Statement 1.4: Design a multi-account AWS environment.

- Based on [**Security** Pillar](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf)
  - **`SEC01-BP01`**(High👀) and **`SEC01-BP02`**(High👀):<br> While it applies to all three skills, it’s because  foundational to [**Multi-account strategy**](https://docs.aws.amazon.com/pdfs/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.pdf) and unavoidable.

|Skills|Related to the best practices of WA-Framework|
|---|---|
| 1. Evaluating the most appropriate account structure for organizational requirements| AWS account management and separation|
|| - **`SEC01-BP01`**(High👀): Separate workloads using accounts|
|| - **`SEC01-BP02`**(High👀): Secure account root user and properties|
|| - - **`SEC03-BP03`**: Establish emergency access process|
|| - - **`SEC03-BP05`**: Define permission guardrails for your organization|
|| - - **`SEC03-BP07`**: Analyze public and cross-account access|
|| - - **`SEC08-BP01`**(High👀): Implement secure key management|
|| - - **`OPS05-BP08`**: Use multiple environments|
|| - - **`SEC10-BP03`**: Prepare forensic capabilities|
| 2. Recommending a strategy for **central logging** and **event notifications**| Configure services and resources centrally|
|| - **`SEC04-BP01`** Configure service and application logging|
|| - **`SEC04-BP02`** Capture logs, findings, and metrics in standardized locations|
|| - - `SEC01-BP01`(High👀): Separate workloads using accounts|
|| - - `SEC06-BP01`(High👀): Perform vulnerability management|
|| - - `OPS08-BP01`: Analyze workload metrics|
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
| 3. Understanding how **purchasing options** affect cost and performance|Select **the best pricing model**|
|| - **`COST07-BP01`**(High👀): Perform **pricing model** analysis|
|| - **`COST07-BP02`**: Choose Regions based on cost|
|| - **`COST07-BP03`**: Select third-party agreements with cost-efficient terms|
|| - **`COST07-BP04`**: Implement **pricing models** for all components of this workload|
|| - **`COST07-BP05`**: Perform **pricing model** analysis at the management account level|

---
