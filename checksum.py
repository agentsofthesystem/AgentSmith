import os
import hashlib


def compute_checksums():
    dist_path = os.path.join("dist", "agent-smith.exe")
    checksum_file = "checksum.txt"

    md5_sum = hashlib.md5(open(dist_path, "rb").read()).hexdigest()
    sha1_sum = hashlib.sha1(open(dist_path, "rb").read()).hexdigest()
    sha256_sum = hashlib.sha256(open(dist_path, "rb").read()).hexdigest()

    if os.path.exists(checksum_file):
        os.remove(checksum_file)

    with open(checksum_file, "w") as f:
        f.write("agent-smith.exe\n\n")
        f.write(f"MD5: {md5_sum}\n")
        f.write(f"SHA1: {sha1_sum}\n")
        f.write(f"SHA256: {sha256_sum}\n")


if __name__ == "__main__":
    compute_checksums()
