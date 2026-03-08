---
title: Lowering the Barrier of Entry for Automated Governance - GitHub's New Artifact Attestation Feature
date: 2024-05-13
author: Eric Chapman
slug: lowering-the-barrier-of-entry-for-automated-governance-github-artifact-attestation-feature
category: platform-devops
tags: [software-supply-chain, governance, github, devsecops, platform-engineering]
excerpt: Explores how GitHub artifact attestation can make governance automation more accessible for enterprise engineering teams.
imported_on: 2026-03-08
import_method: manual_archive_import
needs_review: false
import_notes: Full body provided by author and normalized to markdown.
status: imported
---

GitHub's new Artifact Attestations feature represents a significant advancement for streamlining Governance, Risk, and Compliance (GRC) processes. By integrating attestation creation directly into GitHub Actions, it simplifies automated governance adoption and reduces the need for external tools.

## Introduction

GitHub's recent blog on Artifact Attestations is great news for organizations on the path to automate their Governance, Risk, and Compliance (GRC). Before we dive too deep into GitHub's new Artifact Attestations feature, let's take a step back and do a quick recap of the domain it fits into: Automated Governance.

Automated Governance goes by many aliases, including Governance, Risk, and Compliance (GRC) engineering and policy as code. While industry experts might differentiate between these elements, the desired outcome is the same: improving the security and compliance of artifacts created by software supply chains in an automated fashion.

At a high level, Automated Governance refers to the ability to provide the collection, attestation, policy evaluation, and enforcement of an organization's GRC standards throughout the software development lifecycle. With that in mind, let's talk about why GitHub's Artifact Attestations feature is a big deal and what challenges still exist when implementing Automated Governance.

## GitHub Artifact Attestations: What Excites Us the Most

- Integrating the attestation element of the GRC process in the same platform as SCM, CI/CD, and security validations reduces the need for platform engineering teams to host a Sigstore stack.
- It significantly lowers the barrier of entry for product and platform teams using GitHub to adopt Automated Governance by getting a major component out of the box.
- All that is needed to get started is to add YAML to a GitHub Actions workflow for attestation creation and use the GitHub CLI for verification and policy evaluation.

Reference:

- https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/

GitHub now provides three GitHub Actions:

- `actions/attest-build-provenance`
- `actions/attest-sbom`
- `actions/attest` (generic/extensible for other predicate types)

Prior to this update, teams often had to create their own build images with Sigstore tooling and write custom pipeline automation for collection, attestation, policy evaluation, and enforcement.

The technology and approach are directly aligned with our POV on implementing Automated Governance. GitHub's supported workflow can remove roughly 100 lines of workflow code in a typical implementation. Organizations no longer need to implement custom provenance and SBOM steps when they can call GitHub's actions directly.

GitHub is also hosting a Sigstore instance for private repos, while public repos use Sigstore's public-good instance. This removes another production workload teams would otherwise run and maintain.

GitHub is now an approved root certificate authority. This gives customers and open source projects a path for signing artifacts without building out PKI or managing secrets that could be leaked or lost.

SBOMs can now be associated with an artifact via GitHub's `attest-sbom` action, which wraps a provided SBOM in an in-toto predicate, signs it using GitHub's internal Sigstore, associates it with the artifact, and stores it in GitHub's attestation store.

All of these features accelerate adoption and rollout while helping democratize Automated Governance. This reflects a significant engineering investment and underscores GitHub's commitment to being a top-tier engineering platform.

## Challenges of Automated Governance

Although this is great progress, there are still many challenges organizations must overcome when adopting Automated Governance. The biggest challenge we have encountered in highly regulated enterprises is aligning GRC teams with the technology.

From our experience, auditors and risk owners are not easily excited about CLI tools and CI/CD pipelines; they need to see how GRC engineering makes their job easier by creating a mechanism to summarize the risk profile of an artifact for production with drill-down visibility into actual event occurrence.

## Why Automated Governance Should Be on Your Radar

- Open source usage is widespread in enterprises, and having unforgeable proof that an artifact is from a trusted source is imperative.
- The White House Executive Order (EO 14028) is likely only the beginning of broader cybersecurity requirements. It is currently impacting government contractors and may expand to commercial applications in the near term.
- Lack of visibility into artifacts deployed in production can put organizations at risk. A narrow view into only part of the software supply chain puts the whole delivery system at risk.
- Traditional, often manual, governance processes become bottlenecks and hinder fast iteration. Automated Governance can scale with modern software delivery without sacrificing security.

## Conclusion

GitHub's Artifact Attestations feature is a significant step forward for organizations trying to automate GRC processes. Integrating attestation into GitHub lowers adoption barriers and reduces custom implementation overhead. Out-of-the-box actions for provenance and SBOM checks, plus the extensible generic attest action and future predicate support, make it easier to integrate attestations into existing workflows.

GitHub's role as an approved root certificate authority further strengthens software supply chain trust and security.

Despite these advancements, challenges remain, especially aligning GRC teams with technical implementations. One advantage of running a self-managed Sigstore stack is direct access to all attestations for downstream visualization (for example, with Grafana). GitHub could close this gap further by supporting attestation export or in-platform visualization.

Ultimately, GitHub's investment in Automated Governance reinforces a path where compliance and innovation can coexist at enterprise scale.

Read GitHub's full announcement:

- https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/
