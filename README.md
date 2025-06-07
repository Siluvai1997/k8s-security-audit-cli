# Kubernetes Security Audit CLI Tool

## Project Overview

This project is a **command-line security auditing tool for Kubernetes clusters**. Written in Python using the Kubernetes client API, it scans for common security misconfigurations such as:

- Insecure RBAC roles
- Privileged containers
- Public-facing Services
- Pods running as root
- Missing resource limits

This tool helps DevOps engineers and SREs identify risks in active clusters — perfect for use in audits, compliance checks, or pre-deployment reviews.

---

## Tech Stack

- Python 3.x
- `kubernetes` Python client
- argparse for CLI flags
- Compatible with `kubeconfig` or in-cluster access

---

## Checks Performed

| Check | Description |
|-------|-------------|
| RBAC | Flags ClusterRoles/Bindings with wildcard `*` permissions |
| Privileged Pods | Detects pods with `privileged: true` or `runAsRoot` |
| Public Services | Flags services of type `LoadBalancer` or `NodePort` |
| Resource Limits | Identifies containers missing CPU/memory limits |

---

## How to Use

```
# Install dependencies
pip install -r requirements.txt
```

# Run audit on current context
```
python3 audit/audit.py
```

# Run audit on a specific kubeconfig
```
python3 audit/audit.py --kubeconfig ~/.kube/mycluster-config
```
---

## Sample Output
- ClusterRole 'admin-role' uses '*': overly permissive.
- Pod 'nginx' in ns 'default' runs as privileged.
- Service 'frontend' in ns 'dev' is type NodePort.
- Container in pod 'worker' lacks CPU/memory limits.

---

## Permissions Required
To use this tool, the running user (or service account) must have:
- list/get permissions on:
  - pods
  - roles, rolebindings, clusterroles
  - services
  
---

#### Disclaimer

This is a lightweight scanner for educational/demo purposes. For enterprise use, consider open-source tools like:
- kube-bench
- kube-hunter
- polaris

---
