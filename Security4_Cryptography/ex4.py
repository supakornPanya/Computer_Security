import subprocess
import time
import os

FILE_NAME = "benchmark_data.bin"
FILE_SIZE_MB = 10
FILE_SIZE_BYTES = FILE_SIZE_MB * 1024 * 1024  # Divisible by 8 for Blowfish -nopad

# Common parameters from hint
KEY_HEX = "00112233445566778899aabbccddeeff"
IV_HEX_64BIT = "0123456789abcdef"  # 8 bytes for Blowfish


def setup_test_environment():
    print(f"Creating {FILE_SIZE_MB} MB dummy file...")
    with open(FILE_NAME, "wb") as f:
        f.write(b"\0" * FILE_SIZE_BYTES)


def run_command(cmd_list):
    start = time.perf_counter()
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    duration = time.perf_counter() - start
    if result.returncode != 0:
        # Fallback if legacy provider is not needed
        fallback_cmd = [c for c in cmd_list if c not in ["-provider", "legacy", "default"]]
        start = time.perf_counter()
        result = subprocess.run(fallback_cmd, capture_output=True, text=True)
        duration = time.perf_counter() - start
        if result.returncode != 0:
            print(f"Error running command: {' '.join(cmd_list)}")
            print(f"Stderr: {result.stderr.strip()}")
            return None
    return duration


def benchmark():
    setup_test_environment()
    results = {}

    # 1. SHA-1 Benchmark
    print("Measuring SHA-1...")
    sha1_cmd = ["openssl", "dgst", "-sha1", FILE_NAME]
    t_sha1 = run_command(sha1_cmd)
    if t_sha1:
        mb_per_sec = FILE_SIZE_MB / t_sha1
        results["SHA-1"] = f"{mb_per_sec:.2f} MB/s ({t_sha1:.4f} s)"

    # 2. RC4 Benchmark (Follow hint: -e -in ... -out ... -K ... -nosalt)
    print("Measuring RC4...")
    rc4_cmd = [
        "openssl", "enc", "-rc4",
        "-e",
        "-in", FILE_NAME,
        "-out", "rc4.enc",
        "-K", KEY_HEX,
        "-nosalt",
        "-provider", "legacy",
        "-provider", "default"
    ]
    t_rc4 = run_command(rc4_cmd)
    if t_rc4:
        mb_per_sec = FILE_SIZE_MB / t_rc4
        results["RC4"] = f"{mb_per_sec:.2f} MB/s ({t_rc4:.4f} s)"

    # 3. Blowfish Benchmark (Follow hint: -e -in ... -out ... -K ... -iv ... -nopad -nosalt)
    print("Measuring Blowfish (CBC)...")
    bf_cmd = [
        "openssl", "enc", "-bf-cbc",
        "-e",
        "-in", FILE_NAME,
        "-out", "bf.enc",
        "-K", KEY_HEX,
        "-iv", IV_HEX_64BIT,
        "-nopad",
        "-nosalt",
        "-provider", "legacy",
        "-provider", "default"
    ]
    t_bf = run_command(bf_cmd)
    if t_bf:
        mb_per_sec = FILE_SIZE_MB / t_bf
        results["Blowfish"] = f"{mb_per_sec:.2f} MB/s ({t_bf:.4f} s)"

    # 4. DSA Benchmark (Sign & Verify operations)
    print("Preparing DSA keys and measuring Sign/Verify...")
    subprocess.run(["openssl", "dsaparam", "-out", "dsaparam.pem", "2048"], capture_output=True)
    subprocess.run(["openssl", "gendsa", "-out", "dsa_priv.pem", "dsaparam.pem"], capture_output=True)
    subprocess.run(["openssl", "dsa", "-in", "dsa_priv.pem", "-pubout", "-out", "dsa_pub.pem"], capture_output=True)

    dsa_sign_cmd = ["openssl", "dgst", "-sha1", "-sign", "dsa_priv.pem", "-out", "dsa.sig", FILE_NAME]
    t_dsa_sign = run_command(dsa_sign_cmd)

    dsa_verify_cmd = ["openssl", "dgst", "-sha1", "-verify", "dsa_pub.pem", "-signature", "dsa.sig", FILE_NAME]
    t_dsa_verify = run_command(dsa_verify_cmd)

    if t_dsa_sign and t_dsa_verify:
        results["DSA Sign"] = f"{t_dsa_sign:.4f} s ({1 / t_dsa_sign:.2f} ops/s)"
        results["DSA Verify"] = f"{t_dsa_verify:.4f} s ({1 / t_dsa_verify:.2f} ops/s)"

    # Clean up generated temporary files
    cleanup_files = [
        FILE_NAME, "rc4.enc", "bf.enc", "dsaparam.pem",
        "dsa_priv.pem", "dsa_pub.pem", "dsa.sig"
    ]
    for filename in cleanup_files:
        if os.path.exists(filename):
            os.remove(filename)

    # Print summary table
    print("\n" + "=" * 50)
    print(f"{'Algorithm':<15} | {'Measured Performance':<30}")
    print("=" * 50)
    for algo, metric in results.items():
        print(f"{algo:<15} | {metric:<30}")
    print("=" * 50)


if __name__ == "__main__":
    benchmark()