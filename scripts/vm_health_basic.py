## This is a basic health check script designed to check the health of VMs in inventory on VMware ESXi.
## Note that credentials will need to be provided in a .env file, an example can be found in this same scripts repo.
## This script checks VM power status, VMware Tools Status, CPU Usage, and Memory Usage. Enjoy!

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim 
from dotenv import load_dotenv

import ssl
import os
import atexit
import sys



load_dotenv()

VMWARE_HOST = os.getenv("VMWARE_HOST")
VMWARE_USER = os.getenv("VMWARE_USER")
VMWARE_PASS = os.getenv("VMWARE_PASS")



def validate_env():
    missing = []

    if not VMWARE_HOST:
        missing.append("VMWARE_HOST")
    if not VMWARE_USER:
        missing.append("VMWARE_USER")
    if not VMWARE_PASS:
        missing.append("VMWARE_PASS")
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Check your .env file.")
        sys.exit(1)


def connect_to_vmware():
    context = ssl._create_unverified_context()


    service_instance = SmartConnect(
        host=VMWARE_HOST,
        user=VMWARE_USER,
        pwd=VMWARE_PASS,
        sslContext=context
    )

    atexit.register(Disconnect, service_instance)
    return service_instance


def get_all_vms(content):
    view = content.viewManager.CreateContainerView(
        content.rootFolder,
        [vim.VirtualMachine],
        True
    )

    vms = view.view
    view.Destroy()


    return vms


def check_vm_health(vm):
    issues = []


    name = vm.name
    power_state = vm.runtime.powerState
    tools_status = vm.guest.toolsStatus
    cpu_usage = vm.summary.quickStats.overallCpuUsage
    memory_usage = vm.summary.quickStats.guestMemoryUsage

    if power_state != "poweredOn":
        issues.append("VM is not powered on")


    if tools_status in ["toolsNotInstalled", "toolsNotRunning", "toolsOld"]:
        issues.append(f"VMware Tools Problem: {tools_status}")
    
    if vm.snapshot is not None:
        issues.append("VM has one or more snapshots")

    return {
        "name": name,
        "power_state": power_state,
        "tools_status": tools_status,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "issues": issues
    }


def print_report(vm_results):
    print("\nESXi / Mordor VM Health Report")
    print("=" * 60)


    for result in vm_results:
        status = "OK" if not result["issues"] else "WARNING"

        print(f"\n[{status}] {result['name']}")
        print(f" Power State:    {result['power_state']}")
        print(f" VMware Tools:   {result['tools_status']}")
        print(f" CPU Usage:      {result['cpu_usage']} MHz")
        print(f" Memory Usage:   {result['memory_usage']} MB")


        if result["issues"]:
            print("  Issues")
            for issue in result["issues"]:
                print(f"     - {issue}")


def main():
    validate_env()


    print(f"Connecting to (VMWARE_HOST)...")

    service_instance = connect_to_vmware()
    content = service_instance.RetrieveContent()

    vms = get_all_vms(content)

    vm_results = []

    for vm in vms:
        vm_results.append(check_vm_health(vm))
    
    print_report(vm_results)


if __name__ == "__main__":
    main()
