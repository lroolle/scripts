import argparse
import json


def process_json_file(filename):
    """Read a JSON file, remove 'sp_with_eths' from each item, and write it back."""
    with open(filename, "r") as file:
        data = json.load(file)

    # Assuming the JSON data is a list of dictionaries
    for item in data:
        if "sp_with_eths" in item:
            del item["sp_with_eths"]

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="Remove 'sp_with_eths' field from each item in a JSON file."
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the JSON file.")
    args = parser.parse_args()

    process_json_file(args.file)


if __name__ == "__main__":
    main()
