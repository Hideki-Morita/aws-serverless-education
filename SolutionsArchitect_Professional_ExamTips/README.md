## 🪩 Relationship between SAP Exam and Well-Architected Framework

<br>

Here’s the relational list mapping all domains and task statements from the **AWS Certified Solutions Architect Professional** (SAP-C02) Exam Guide to the <mark>**AWS Well-Architected Framework**</mark> principles:

---

<br>

### ☻ Domain 1: Design Solutions for Organizational Complexity

<br>

---

<br>

#### ✰ Task Statement 1.1: Architect _network connectivity_ strategies.

Skills in:  
	•	Evaluating connectivity options for multiple VPCs  
	  •	`REL02-BP03`: Ensure IP subnet allocation accounts for expansion and availability.  
	•	Evaluating connectivity options for on-premises, co-location, and cloud integration  
	  •	`REL02-BP02`: Provision redundant connectivity between private networks in the cloud and on-premises environments.  
	•	Designing hybrid networking solutions  
	  •	`REL02-BP01`: Use highly available network connectivity for your workload public endpoints.  

Task Statement 1.2: Prescribe security controls.

Skills in:
	•	Designing access control mechanisms
	•	SEC01-BP03: Implement least privilege access control for all systems.
	•	Protecting data at rest and in transit
	•	SEC02-BP04: Use AWS-managed encryption wherever possible.
	•	Monitoring and incident response
	•	SEC03-BP05: Define and practice incident response procedures.

Task Statement 1.3: Design reliable and resilient architectures.

Skills in:
	•	Implementing fault-tolerant systems
	•	REL01-BP01: Design for failure by using redundancy and automatic recovery.
	•	Applying disaster recovery techniques
	•	REL05-BP01: Use a disaster recovery plan with clearly defined recovery objectives.

Task Statement 1.4: Design a multi-account AWS environment.

Skills in:
	•	Structuring accounts using AWS Organizations
	•	OP04-BP03: Use a multi-account strategy for workload isolation.
	•	Centralized governance
	•	SEC05-BP02: Aggregate logs across accounts for centralized monitoring.

Task Statement 1.5: Determine cost optimization and visibility strategies.

Skills in:
	•	Optimizing resource utilization
	•	COST01-BP01: Use Auto Scaling to match capacity to demand.
	•	Tracking costs using tags
	•	COST02-BP02: Implement cost allocation tags to track resource usage.
	•	Leveraging reserved instances
	•	COST03-BP03: Use Reserved Instances or Savings Plans for predictable workloads.

Domain 2: Design for New Solutions

Task Statement 2.1: Define secure application architectures.

Skills in:
	•	Implementing IAM for secure access
	•	SEC01-BP01: Manage application permissions securely using roles and policies.
	•	Encrypting data and monitoring access
	•	SEC02-BP03: Enable logging for data access monitoring.

Task Statement 2.2: Design high-performance architectures.

Skills in:
	•	Optimizing compute resources
	•	PERF02-BP01: Choose the optimal compute service for your workload.
	•	Implementing efficient data storage
	•	PERF03-BP02: Use SSDs or memory-optimized instances where applicable.
	•	Improving latency with caching
	•	PERF04-BP02: Use caching to improve response times.

Task Statement 2.3: Architect cost-efficient solutions.

Skills in:
	•	Selecting storage classes
	•	COST01-BP04: Optimize storage by selecting the right class and configuration.
	•	Minimizing transfer costs
	•	COST02-BP03: Use Amazon CloudFront to reduce data transfer expenses.

Task Statement 2.4: Design sustainable architectures.

Skills in:
	•	Reducing energy consumption
	•	SUS01-BP02: Use serverless architectures to minimize resource usage.
	•	Deploying in renewable energy regions
	•	SUS02-BP03: Utilize regions with AWS renewable energy initiatives.

Domain 3: Continuous Improvement for Existing Solutions

Task Statement 3.1: Implement secure and compliant workloads.

Skills in:
	•	Automating compliance checks
	•	SEC04-BP01: Use AWS Config to automate compliance checks.
	•	Protecting sensitive workloads
	•	SEC02-BP02: Apply appropriate encryption and data protection.

Task Statement 3.2: Optimize workload performance.

Skills in:
	•	Analyzing and improving system performance
	•	PERF01-BP03: Continuously monitor and optimize your workloads.
	•	Optimizing storage solutions
	•	PERF03-BP03: Use lifecycle policies for storage optimization.

Task Statement 3.3: Implement cost optimization strategies.

Skills in:
	•	Rightsizing compute resources
	•	COST01-BP02: Select the appropriate instance size for your workload.
	•	Using cost monitoring tools
	•	COST02-BP01: Leverage AWS Cost Explorer for visibility into usage patterns.

Domain 4: Accelerate Workload Migration and Modernization

Task Statement 4.1: Design migration strategies.

Skills in:
	•	Using migration tools
	•	REL04-BP03: Use AWS Migration Hub to orchestrate migrations.
	•	Minimizing downtime
	•	REL04-BP02: Use failover or replication strategies to reduce migration impacts.

Task Statement 4.2: Modernize legacy workloads.

Skills in:
	•	Rearchitecting applications for cloud-native services
	•	PERF02-BP04: Modernize applications by leveraging managed services.
	•	Adopting serverless and microservices
	•	SUS01-BP01: Transition workloads to serverless for better efficiency.

