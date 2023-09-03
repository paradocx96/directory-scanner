def increment_patch(version):
    major, minor, patch = version.split('.')
    patch = int(patch) + 1
    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":
    current_version = "1.0.0"
    new_version = increment_patch(current_version)
    with open("version.txt", "w") as f:
        f.write(new_version)
