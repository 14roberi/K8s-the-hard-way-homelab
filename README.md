# K8s-the-hard-way-homelab

## Overview

This repository documents my Kubernetes-The-Hard-Way homelab deployment running on VMware ESXi in a segmented enterprise-style lab environment.

The goal of this project is to develop hands-on experience with:

- Kubernetes internals
- Linux administration
- Infrastructure as Code (IaC)
- Networking and VLAN segmentation
- Container runtimes
- Automation with Ansible and Python
- Monitoring and observability
- Git/GitHub workflows
- Platform engineering concepts

This environment is intentionally being built manually to better understand how Kubernetes components interact under the hood.

---

# Lab Environment

## Hypervisor Platform

- VMware ESXi 8
- vCenter Server Appliance (VCSA)
- HP ProLiant DL360p Gen8

## Networking

- FortiGate 40F Firewall
- Netgear Managed Switch
- VLAN Segmentation
- Static IP Addressing
- Internal RFC1918 Address Space

## Kubernetes Network

| VLAN | Purpose | Subnet |
|------|----------|---------|
| VLAN xx | Kubernetes Cluster | 192.168.10.1/24 |

---

# Cluster Architecture

## Control Plane

| Hostname | IP Address |
|----------|-------------|
| k8s-cp-1 | 192.168.10.20 |

## Worker Nodes

| Hostname | IP Address |
|----------|-------------|
| k8s-node-1 | 192.168.10.30 |
| k8s-node-2 | 192.168.10.40 |

---

# Technologies Used

- Kubernetes
- containerd
- etcd
- Linux (Debian)
- VMware ESXi
- vCenter
- FortiGate
- Git/GitHub
- Ansible
- Python
- YAML
- Bash scripting

---

# Repository Structure

```text
kubernetes-the-hard-way-homelab/
│
├── docs/
├── diagrams/
├── ansible/
├── terraform/
├── kubernetes/
├── scripts/
├── screenshots/
└── troubleshooting/
