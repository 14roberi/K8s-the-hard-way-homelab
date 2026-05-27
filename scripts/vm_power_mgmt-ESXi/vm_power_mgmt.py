## NOTE, the "power off" option in this script is a hard shutdown not a graceful shutdown of the guest OS. I will be adding that feature momentarily ##

import os
import ssl
from pathlib import Path
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTask
from pyVmomi import vmodl 
from pyVmomi import vim
import atexit
import logging
from datetime import datetime


# Create Logs directory if it doesn't exist
log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(exist_ok=True)

# Log file with date/time stamp
log_file = log_dir / f"vm_power_mgmt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure Logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

print(f"Logging to: {log_file}")
logging.info("Starting VM Power Management Script")


def get_all_vms(content):
    container = content.viewManager.CreateContainerView(
        content.rootFolder,
        [vim.VirtualMachine],
        True
    )

    vms = list(container.view)
    container.Destroy()
    
    return sorted(vms, key=lambda vm: vm.name.lower())


def print_vm_health_report(vm):
    print(f"Name: {vm.name}")
    print(f"Power State: {vm.runtime.powerState}")
    print(f"Guest OS: {vm.config.guestFullName if vm.config else 'Unknown'}")
    print(f"IP Address: {vm.guest.ipAddress if vm.guest else 'Unknown'}")
    print(f"VMware Tools: {vm.guest.toolsStatus if vm.guest else 'Unknown'}")
    print(f"CPU Count: {vm.config.hardware.numCPU}")
    print(f"Memory MB: {vm.config.hardware.memoryMB}")
    print(f"Host: {vm.runtime.host.name if vm.runtime.host else 'Unknown'}")
    



def display_vm_inventory(vms):
    print(f"\nVm Inventory")
    print("-" * 60)

    vm_map = {}

    for index, vm in enumerate(vms, start=1):
        vm_map[index] = vm
        power_state = vm.runtime.powerState
        guest_os = vm.config.guestFullName if vm.config else "Unknown"

        print(f"{index}. {vm.name:<25} {power_state:<12} {guest_os}")
    
    return vm_map


def choose_vm(vm_map):
    vm_choice = input(
        "\nSelect VM number from inventory list or type 'q' to exit: "
    ).strip().lower()

    if vm_choice in ['q', 'quit', 'exit']:
        return "exit"

    if not vm_choice.isdigit() or int(vm_choice) not in vm_map:
        print("Invalid VM Selection")
        return None
    
    return vm_map[int(vm_choice)]


def choose_action():
    print("\nChoose an action:")
    print("1. Power On")
    print("2. Power Off")
    print("3. Reset")
    print("4. Health Report")
    print("5. Snapshots")
    print("6. Exit")

    choice = input("\nSelect Action: ").strip()

    actions = {
        "1": "power_on",
        "2": "power_off",
        "3": "reset",
        "4": "health_report",
        "5": "snapshots",
        "6": "exit"
    }

    return actions.get(choice)

    
def perform_action(vm, action):
    power_state = vm.runtime.powerState

    if action == "power_on":
        if power_state != vim.VirtualMachine.PowerState.poweredOn:
             print(f"Powering on {vm.name}...")
             logging.info(f"Attempting to power on VM: {vm.name}")
             task = vm.PowerOn()
             WaitForTask(task)
             print(f"{vm.name} powered on successfully")
             logging.info(f"Successfully powered on VM: {vm.name}")
        else:
             print(f"{vm.name} is already powered on")

    elif action == "power_off":
        if power_state == vim.VirtualMachine.PowerState.poweredOn:
            print(f"Powering off {vm.name}...")
            logging.info(f"Attempting to power off VM: {vm.name}")
            task = vm.PowerOff()
            WaitForTask(task)
            print(f"{vm.name} powered off successfully")
            logging.info(f"Successfully powered off VM: {vm.name}")
        else:
            print(f"{vm.name} is already powered off.")

    elif action == "reset":
        if power_state == vim.VirtualMachine.PowerState.poweredOn:
            print(f"Resetting {vm.name}...")
            logging.info(f"Attempting to reset VM: {vm.name}")
            task = vm.Reset()
            WaitForTask(task)
            print(f"{vm.name} reset successfully")
            logging.info(f"Successfully reset VM: {vm.name}")
        else:
            print(f"{vm.name} Must be powered on to reset.")

    elif action == "health_report":
        print_vm_health_report(vm)
    
    elif action == "snapshots":
        snapshot_name = input("Enter snapshot name: ").strip()
        snapshot_desc = input("Enter snapshot description: ").strip()
    
        if not snapshot_name:
            print("Snapshot name cannot be empty.")
            return

        print(f"Creating snapshot for {vm.name}....")
        task = vm.CreateSnapshot_task(
            name=snapshot_name,
            description=snapshot_desc,
            memory=False,
            quiesce=False
        )

        WaitForTask(task)
        print(f"Snapshot '{snapshot_name}' created for {vm.name}.")
        logging.info(f"Created snapshot '{snapshot_name}' for VM: {vm.name}")


 
def main():
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)

    print(f"Loading .env from: {env_path}")
    print(f".env exists: {env_path.exists()}")

    esxi_host = os.getenv("ESXI_HOST")
    esxi_user = os.getenv("ESXI_USER")
    esxi_password = os.getenv("ESXI_PASSWORD")
    disable_ssl = os.getenv("ESXI_DISABLE_SSL_VERIFY", "false").lower() == "true"

    if not all([esxi_host, esxi_user, esxi_password]):
        raise ValueError("Missing ESXI_HOST, ESXI_USER, ESXI_PASSWORD in .env")

    ssl_context = None
    if disable_ssl:
        ssl_context = ssl._create_unverified_context()

    service_instance = SmartConnect(
        host=esxi_host,
        user=esxi_user,
        pwd=esxi_password,
        sslContext=ssl_context
    )

    atexit.register(Disconnect, service_instance)

    content = service_instance.RetrieveContent()

    while True:
        vms = get_all_vms(content)

        if not vms:
            print("No VMs found on this ESXi host.")
            break
    
        vm_map = display_vm_inventory(vms)
    
        selected_vm = choose_vm(vm_map)

        if isinstance(selected_vm, str) and selected_vm == "exit":
            print("Exiting...")
            logging.info("User exited from VM Inventory menu")
            logging.info("Exiting VM Power Management Script")
            break

        if not selected_vm:
            continue
    
        print(f"\nSelected VM: {selected_vm.name}")

        action = choose_action()

        if not action:
            print("Invalid action.")
            continue

        if action == "exit":
            print("Exiting...")
            logging.info("Exiting VM Power Management Script")
            break
        try:
            perform_action(selected_vm, action)
        except vmodl.MethodFault as e:
            print(f"vSphere error: {e.msg}")
            logging.error(f"ESXi error: {e.msg}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logging.error(f"Unexpected error on VM: {selected_vm.name} - {e}")


if __name__ == "__main__":
    main()
