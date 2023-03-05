import os
import hashlib
import requests


def get_expected_sha256(version):
    url = f"http://download.videolan.org/pub/videolan/vlc/{version}/SHA256SUMS"
    response = requests.get(url)
    expected_hash = response.content.decode("utf-8")
    expected_hash = expected_hash.split()[0]  # take only the hash value
    return expected_hash


def download_installer(version):
    url = f"http://download.videolan.org/pub/videolan/vlc/{version}/win64/vlc-3.0.17-win64.exe"
    response = requests.get(url)
    return response.content


def calculate_sha256(data):
    hash_object = hashlib.sha256()
    hash_object.update(data)
    return hash_object.hexdigest()


def installer_ok(installer_data, expected_hash):
    calculated_hash = calculate_sha256(installer_data)
    return calculated_hash == expected_hash


def save_installer(installer_data):
    temp_folder = os.getenv("TEMP")
    installer_path = os.path.join(temp_folder, "vlc_installer.exe")
    with open(installer_path, "wb") as f:
        f.write(installer_data)
    return installer_path


def run_installer(installer_path):
    os.system(f"{installer_path} /S")


def delete_installer(installer_path):
    os.remove(installer_path)


def main():
    version = "3.0.17.4"
    installer_data = download_installer(version)
    expected_sha256 = get_expected_sha256(version)
    if installer_ok(installer_data, expected_sha256):
        installer_path = save_installer(installer_data)
        run_installer(installer_path)
        delete_installer(installer_path)
    else:
        print("Installer download failed verification. Aborting installation.")


if __name__ == "__main__":
    main()
