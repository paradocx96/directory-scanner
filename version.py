def read_version():
    with open('version.txt', 'r') as file:
        return file.read().strip()


def write_version(updated_version):
    with open('version.txt', 'w') as file:
        file.write(updated_version)


def increment_patch(version):
    major, minor, patch = version.split('.')
    patch = int(patch) + 1
    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":
    # Read the current version
    current_version = read_version()

    # Increment the patch version
    new_version = increment_patch(current_version)

    # Write the new version
    write_version(new_version)
    print(new_version)
