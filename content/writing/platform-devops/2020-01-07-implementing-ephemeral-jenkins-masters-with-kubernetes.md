---
title: Implementing Ephemeral Jenkins Masters with Kubernetes
date: 2020-01-07
author: Eric Chapman
slug: implementing-ephemeral-jenkins-masters-with-kubernetes
category: platform-devops
tags: [jenkins, kubernetes, ci-cd, platform-engineering, devops]
excerpt: How enterprises can use containers and Kubernetes to build a stable, scalable CI/CD model with ephemeral Jenkins masters.
imported_on: 2026-03-08
import_method: manual_archive_import
needs_review: false
import_notes: Full body provided by author and normalized to markdown.
status: imported
---

We'll show how enterprises can leverage containers to create a stable and scalable CI/CD environment using ephemeral Jenkins masters with Kubernetes.

In conjunction with the recent release of *The Rise of Skywalker*, I figured an image of stormtroopers was in order. What could better represent ephemeral Jenkins build agents than the massive unending population of stormtroopers who lead short-lived lives?

Here's the problem: many organizations run a single Jenkins master and a limited number of build agents with no ability to auto-scale Jenkins to meet delivery team demands. The DevOps team is left guessing how many build agents are needed, and as more teams onboard, bottlenecks appear quickly.

In this post, I review that Jenkins challenge and propose a container-based solution for ephemeral Jenkins masters on Kubernetes.

## The Jenkins Problem

In many organizations, Jenkins is implemented using one of two models:

1. Centralized management (top-down)
2. Individual team management (grassroots)

### Centralized Management

This approach deploys one Jenkins master with multiple agents, usually managed by a centralized team that tries to support all team pipeline permutations.

In practice, this does not scale well as CI/CD demand grows. Building and maintaining the full matrix of plugins, agent images, and runtime requirements becomes high risk. A single centralized master is also a single point of failure: if it goes down, all teams stop building, testing, and deploying.

Just as importantly, heavy central control can inhibit product team innovation. Teams cannot easily experiment with plugins or process changes without approval queues.

### Individual Team Management

This model lets each team manage its own Jenkins master and agents. It solves many configuration and autonomy problems, but scalability remains a challenge.

It also assumes each team has:

- Jenkins administration skills
- time to maintain masters and agents
- infrastructure ownership capability

At enterprise scale, this creates consistency issues and fragmented delivery patterns.

Regardless of model, physical host/VM-based Jenkins often results in overprovisioning or underutilization. It's a guessing game: either excess compute or build queue pain.

## The Jenkins Solution

Organizations have many CI/CD options, but open source Jenkins remains one of the most robust orchestrators for complex enterprise delivery.

The key requirement is dynamic scaling.

We recommend running Jenkins using a container-based approach on Kubernetes:

- better portability and fidelity from development to production
- rapid scaling under load or failure
- higher density and lower operational cost using platforms such as AKS, EKS, GKE, and OpenShift

The rest of this guide describes how to use ephemeral Jenkins masters with Kubernetes to create a stable, scalable, and empowering CI/CD environment.

## Ephemeral Jenkins Implementation Overview

### Assumptions

- Teams are already familiar with creating and editing Jenkinsfiles.
- Jenkins master recipients (business unit, enablement team, or delivery team) accept maintenance responsibility.
- Teams have limited direct master management; plugin/config changes flow through InnerSource.
- Jenkins Configuration as Code is used for master configuration.
- Jenkins logs are persisted in a logging platform such as ELK.
- Pipeline stage executions are not memory-intensive (for example, less than 4GB limits in some configurations).
- A managed Kubernetes service is already in place.

### Recommendations

- Implementation strategy should match enterprise maturity.
- Early in transformation, centralized management may still be necessary.
- As maturity grows, ownership can move to business units or delivery teams.
- Start all Jenkins masters from the same base image.
- Persist changes only through pull requests to the base master branch.
- Use API-based secret management (for example, HashiCorp Vault).
- Provide default Jenkinsfile templates when teams are not ready for full ownership.
- Define both Kubernetes and Jenkins infrastructure as code.
- Use Terraform to manage and compare state before rollout.

## When an Enterprise Should Consider Ephemeral Jenkins Masters

### Scenario One

Start with a centralized model, then scale out to multiple masters over time. Early DevOps transformations are often centralized until community capability grows.

### Scenario Two

With an enablement mechanism such as a Dojo, delivery teams can learn to administer their own master safely.

## Implementation Details

We recommend ephemeral Jenkins masters and agents per product/business unit on Kubernetes.

This increases team autonomy on plugin choices and availability while preserving baseline standardization.

### Jenkins Guidelines

- Provide declarative pipelines in an InnerSource hub for current tech stacks.
- Reduce plugin dependence by using function-based builder images where possible.
- Keep shared libraries open across the enterprise.
- Discourage manual config and customization plugins.
- Declare changes as source via Configuration as Code.
- Integrate security scanning (container, SAST, DAST, IAST) directly in pipelines.
- Run stages in technology-specific containers (for example, Maven or NodeJS).
- Maintain a centrally owned base Jenkins master container.
- Maintain centrally owned base technology containers.
- Enable local containerized build/test loops for product teams.
- At end of CI, produce versioned artifacts (binary + container image) and push to artifact storage.

### Kubernetes Guidelines

- Ensure Jenkins pipelines execute in Kubernetes containers.
- Source-control cluster config and deployment scripting.
- Give each product team its own namespace.
- Isolate shared services like Vault/Consul in dedicated namespaces.
- Use a system namespace for shared platform resources.
- Prefer managed Kubernetes services where possible.

## Implementation Results

### Jenkins Pipeline Results

- Teams gain more autonomy over Jenkins configuration and plugin decisions.
- Declarative, technology-based pipelines improve consistency.
- Teams can run automated performance/regression suites on demand.
- Security scanning can run on every build via shared library controls.

### Kubernetes/Jenkins Results

- Teams get scalable on-demand build capacity.
- A centralized tools team controls base master standards.
- Product teams can contribute updates through InnerSource pull requests.
- Distributed masters reduce blast radius of outages.
- The DevOps tools organization can scale support across the enterprise.

In the next post in this series, I go deeper on implementing ephemeral Jenkins masters with Kubernetes.
