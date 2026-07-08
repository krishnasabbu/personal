Enterprise Infrastructure Ontology Generator for Existing Application

Objective

I already have a complete enterprise application with the source code, backend APIs, database entities, DTOs, configuration, deployment information, React UI, and infrastructure metadata.

Do NOT create a new data model.

Instead, inspect the existing project and automatically discover the ontology from the current implementation.

The goal is to build an Enterprise Infrastructure Ontology that represents the complete application, infrastructure, dependencies, ownership, and runtime topology.

⸻

Phase 1 - Repository Discovery

Perform a complete analysis of the repository.

Inspect and understand all existing artifacts before generating anything.

Analyze:

* Spring Boot Entities
* JPA/Hibernate Models
* MongoDB Documents (if applicable)
* DTOs
* REST Controllers
* Service Classes
* Repository Classes
* Configuration Files
* Kubernetes YAML
* Dockerfiles
* Helm Charts
* application.yml / application.properties
* Terraform / CloudFormation (if available)
* Jenkins / GitHub Actions
* React Components
* React Flow Components
* Existing API contracts
* Existing Graph/Topology implementations
* Logging
* Monitoring integrations
* Security configuration
* Database schema
* Messaging configuration
* Cache configuration

Build a repository inventory before generating the ontology.

⸻

Phase 2 - Discover Existing Business Objects

Automatically identify all business objects.

Examples:

Applications

Modules

Microservices

Services

Controllers

Database Tables

Entities

Repositories

Jobs

Schedulers

Queues

Topics

Caches

External APIs

Storage

Compute Resources

Deployment Units

Clusters

Nodes

Regions

Zones

Datacenters

Environment

Owners

Teams

Do not hardcode these.

Extract them from the existing codebase.

⸻

Phase 3 - Discover Relationships

Infer relationships from the implementation.

Examples:

Application
runsOn
Deployment

Deployment
hostedIn
Cluster

Cluster
locatedIn
Zone

Zone
locatedIn
Datacenter

Application
dependsOn
Database

Application
dependsOn
Kafka

Application
dependsOn
Redis

Application
communicatesWith
External API

Application
ownedBy
Team

Application
monitoredBy
Monitoring

Application
securedBy
Identity Provider

Application
storesDataIn
Storage

Deployment
exposes
Network Endpoint

Do not invent relationships.

Infer them from:

* Dependency Injection
* Spring Beans
* REST calls
* OpenFeign
* WebClient
* Kafka Producers
* Kafka Consumers
* RabbitMQ
* JMS
* Database access
* Repository usage
* Configuration
* Kubernetes
* Docker
* Terraform
* Environment variables

⸻

Phase 4 - Build Ontology

Generate an ontology with the following node categories.

Application

Deployment

Microservice

API

Controller

Service

Repository

Database

Table

Storage

Queue

Topic

Cache

External API

Compute

Container

Pod

VM

Node

Cluster

Zone

Datacenter

Region

Cloud Provider

Environment

Owner

Team

Monitoring

Alert

Metric

Log

Runbook

Incident

Configuration

Secret

Network Endpoint

DNS

Load Balancer

Every node must have:

id

name

type

category

description

metadata

attributes

relationships

source file

line number (where possible)

⸻

Phase 5 - React Flow Visualization

Create a professional React Flow visualization.

Use custom node types.

Node categories should have different colors/icons.

Examples:

Blue
Applications

Green
Infrastructure

Purple
Storage

Orange
Messaging

Red
Incidents

Gray
Configuration

Yellow
Network

The graph should support:

* Zoom
* MiniMap
* Controls
* Background Grid
* Search
* Expand/Collapse
* Grouping
* Auto Layout (Dagre or ELK)
* Filtering
* Highlight Dependencies
* Highlight Runtime Path
* Highlight Hosting Path
* Highlight Ownership
* Hover Details
* Click to Open Details
* Context Menu
* Fullscreen

⸻

Phase 6 - Graph Layout

Organize the graph into layers.

Business Layer

↓

Application Layer

↓

Deployment Layer

↓

Infrastructure Layer

↓

Location Layer

↓

Physical Layer

Dependencies should be drawn separately from hosting relationships.

Different edge colors:

runsOn

hostedIn

locatedIn

dependsOn

communicatesWith

owns

securedBy

storesDataIn

publishesTo

consumesFrom

Use edge labels.

⸻

Phase 7 - Ontology Explorer

Create a left-side explorer panel.

Support search by:

Application

API

Database

Controller

Service

Topic

Queue

Storage

Environment

Team

Owner

Cluster

Node

Zone

Datacenter

⸻

Phase 8 - Details Panel

Selecting a node should display:

Overview

Attributes

Relationships

Dependencies

Hosting Path

Ownership

Configuration

Metrics

Logs

Alerts

Incidents

Source Code References

API Endpoints

Database Tables

Deployment Information

⸻

Phase 9 - Smart Queries

Generate ontology traversal functions.

Examples:

Where is Application X running?

Which applications depend on Kafka?

Which applications use PostgreSQL?

Which applications are deployed in Production?

Which applications are in Zone A?

Which APIs communicate with Service Y?

What breaks if Database X goes down?

Who owns Application X?

Which applications use Redis?

Show deployment topology of Application X.

Show runtime dependency graph.

Show infrastructure topology.

Show complete impact analysis.

⸻

Phase 10 - Validation

Before generating the ontology:

Validate every discovered node.

Remove duplicates.

Merge aliases.

Resolve circular references.

Verify every relationship exists in the actual codebase.

Do not fabricate infrastructure.

Only generate ontology objects that can be verified from the repository.

Produce a validation report showing:

* discovered nodes
* inferred relationships
* missing metadata
* uncertain mappings
* recommendations

⸻

Deliverables

Generate:

1. Ontology JSON
2. React Flow node definitions
3. React Flow edge definitions
4. Ontology builder service
5. Graph traversal service
6. Search service
7. Layout engine integration
8. TypeScript interfaces
9. React components
10. Documentation explaining how every ontology node was discovered from the existing codebase.

The implementation must be completely data-driven and automatically regenerate the ontology whenever the repository changes, without requiring hardcoded mappings.