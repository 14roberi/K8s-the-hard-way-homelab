import yaml
import sys
from pathlib import Path


def validate_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            yaml.safe_load(file)

        print(f"[SUCCESS] {file_path} is valid YAML.")

    except yaml.YAMLError as e:
        print(f"[ERROR] YAML validation failed for {file_path}")
        print(e)

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")

    except Exception as e:
        print(f"[ERROR] Unexpected error:")
        print(e)


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python3 yaml_validator.py <yaml_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"[ERROR] File does not exist: {file_path}")
        sys.exit(1)

    validate_yaml(file_path)


if __name__ == "__main__":
    main()