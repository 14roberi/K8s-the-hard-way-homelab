# Kubernetes The Hard Way Homelab

Enterprise-style Kubernetes homelab environment built on VMware ESXi using Debian Linux, Ansible automation, and infrastructure engineering best practices.

This repository documents my ongoing work building and automating a self-managed Kubernetes environment inspired by Kubernetes The Hard Way. The goal of this project is to gain hands-on experience with Kubernetes internals, Linux administration, networking, virtualization, infrastructure automation, and DevOps workflows.

---

# Project Goals

- Build Kubernetes manually to better understand cluster internals
- Develop infrastructure automation skills using Ansible
- Practice Linux systems administration and troubleshooting
- Learn Kubernetes networking concepts
- Build reusable automation scripts and tooling
- Simulate enterprise infrastructure workflows in a homelab environment
- Improve operational documentation and Git/GitHub workflows

---

# Environment Overview

## Infrastructure

- VMware ESXi 8.0.3
- HP ProLiant DL360p Gen8
- FortiGate 40F Firewall
- Netgear Managed Switch
- Debian Linux Virtual Machines

## Technologies Used

- Kubernetes
- Ansible
- YAML
- Python
- Linux Networking
- VMware vSphere
- Git / GitHub
- SSH Automation

---

# Lab Architecture

## Current Node Layout

| Hostname | Role |
|---|---|
| server | Kubernetes Control Plane |
| node0 | Kubernetes Worker Node |
| node1 | Kubernetes Worker Node |
| jumpbox | Ansible / Management Node |

---

# Repository Structure

```text
.
├── ansible/
│   ├── inventory.ini
│   ├── ansible.cfg
│   ├── playbooks/
│   ├── group_vars/
│   ├── host_vars/
│   ├── templates/
│   ├── files/
│   └── roles/
│
├── scripts/
│   ├── esxi-health-check/
│   ├── yaml-validator/
│   └── future-tools/
│
├── docs/
├── diagrams/
├── screenshots/
├── troubleshooting/
├── requirements.txt
└── README.md
```

---

# Automation Projects

## ESXi VM Health Check

Python-based utility used to validate:
- VM power states
- VMware connectivity
- Guest operating system status
- Basic VM health metrics

---

## YAML Validator

Python script used to validate YAML syntax before Ansible deployment.

---

## Network Validation Playbook

Ansible-based network diagnostics utility used to validate:
- IP addressing
- Routing tables
- Host configuration
- Traceroute connectivity
- DNS configuration

---

# Example Ansible Usage

## Run Network Validation Playbook

```bash
ansible-playbook -i inventory.ini playbooks/network-check.yml
```

## Run Ansible Connectivity Test

```bash
ansible k8s -i inventory.ini -m ping
```

---

# Python Dependencies

Install Python requirements:

```bash
pip3 install -r requirements.txt
```

---

# System Dependencies

Install required Linux packages:

```bash
sudo apt update
sudo apt install traceroute dnsutils -y
```

---

# Screenshots

## ESXi Environment



---

## Ansible Network Validation



---

# Lessons Learned

This project has helped strengthen understanding of:

- Linux systems administration
- Kubernetes architecture
- Infrastructure automation
- VMware virtualization
- SSH automation
- YAML syntax and validation
- Git/GitHub workflows
- Network troubleshooting
- Infrastructure documentation

---

# Future Improvements

Planned additions to this environment include:

- High Availability Kubernetes control plane
- Helm deployments
- Terraform integration
- GitOps workflows
- Prometheus and Grafana monitoring
- CI/CD pipeline automation
- VMware API automation using pyVmomi
- Additional Ansible roles and reusable playbooks

---

# Security Notes

Sensitive files are excluded from version control using `.gitignore`, including:

- `.env`
- SSH private keys
- kubeconfig files
- API credentials
- secret manifests

---

# References

- Kubernetes The Hard Way  
  https://github.com/kelseyhightower/kubernetes-the-hard-way

- Ansible Documentation  
  https://docs.ansible.com/

- Kubernetes Documentation  
  https://kubernetes.io/docs/

---

# Disclaimer

This repository is intended for educational, homelab, and infrastructure learning purposes.