import argparse
from kubernetes import client, config

def check_rbac():
    print("\n Checking RBAC roles for wildcards...")
    rbac = client.RbacAuthorizationV1Api()
    roles = rbac.list_cluster_role()
    for role in roles.items:
        for rule in role.rules:
            if "*" in rule.verbs or "*" in rule.resources:
                print(f"[!] ClusterRole '{role.metadata.name}' uses '*': overly permissive.")

def check_privileged_pods():
    print("\n Checking for privileged pods or pods running as root...")
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        for container in pod.spec.containers:
            security = container.security_context
            if security:
                if getattr(security, "privileged", False):
                    print(f"[!] Pod '{pod.metadata.name}' in ns '{pod.metadata.namespace}' is privileged.")
                if getattr(security, "run_as_user", 0) == 0:
                    print(f"[!] Pod '{pod.metadata.name}' in ns '{pod.metadata.namespace}' runs as root.")

def check_public_services():
    print("\n Checking for public-facing services...")
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces()
    for svc in services.items:
        svc_type = svc.spec.type
        if svc_type in ["LoadBalancer", "NodePort"]:
            print(f"[!] Service '{svc.metadata.name}' in ns '{svc.metadata.namespace}' is type {svc_type}.")

def check_resource_limits():
    print("\n Checking for missing resource limits...")
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        for container in pod.spec.containers:
            limits = container.resources.limits
            if not limits:
                print(f"[!] Container in pod '{pod.metadata.name}' (ns: {pod.metadata.namespace}) lacks resource limits.")

def main():
    parser = argparse.ArgumentParser(description='Kubernetes Security Audit CLI Tool')
    parser.add_argument('--kubeconfig', help='Path to kubeconfig file (optional)')
    args = parser.parse_args()

    if args.kubeconfig:
        config.load_kube_config(config_file=args.kubeconfig)
    else:
        config.load_kube_config()

    check_rbac()
    check_privileged_pods()
    check_public_services()
    check_resource_limits()

if __name__ == "__main__":
    main()