import os
import ssl

from pathlib import Path
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit


def get_all_vms(content):
    container = content.viewManager.CreateContainerView(
        content.rootFolder,
        [vim.VirtualMachine],
        True
    )

    vms = container.view
    container.Destroy()
    return vms


def wait_for_task(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass

    if task.info.state == vim.TaskInfo.State.error:
        raise Exception(task.info.error.msg)


def main():
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)

    print(f"Loading .env from: {env_path}")
    print(f".env exists: {env_path.exists()}")

    esxi_host = os.getenv("ESXI_HOST")
    esxi_user = os.getenv("ESXI_USER")
    esxi_password = os.getenv("ESXI_PASSWORD")
    disable_ssl = os.getenv("ESXI_DISABLE_SSL_VERIFY", "false").lower() == "true"

    vm_names_raw = os.getenv("VM_NAMES", "")
    target_vm_names = [name.strip() for name in vm_names_raw.split(",") if name.strip()]

    if not all([esxi_host, esxi_user, esxi_password]) or not target_vm_names:
        raise ValueError("Missing ESXI_HOST, ESXI_USER, ESXI_PASSWORD, or VM_NAMES in .env")

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
    all_vms = get_all_vms(content)

    vm_lookup = {vm.name: vm for vm in all_vms}

    print("\nESXi VM Power-On Script")
    print("-" * 30)

    for vm_name in target_vm_names:
        vm = vm_lookup.get(vm_name)

        if not vm:
            print(f"[NOT FOUND] {vm_name}")
            continue

        power_state = vm.runtime.powerState

        if power_state == vim.VirtualMachinePowerState.poweredOn:
            print(f"[ALREADY ON] {vm_name}")
        else:
            print(f"[POWERING ON] {vm_name}")
            task = vm.PowerOn()
            wait_for_task(task)
            print(f"[SUCCESS] {vm_name} is now powered on")

    print("\nDone.")


if __name__ == "__main__":
    main()



