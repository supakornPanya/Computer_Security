import subprocess
import os

def run_cmd(cmd):
    print(f"[RUN] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] {res.stderr}")
    return res

def main():
    # 1. Convert image to 2000x2000 PBM (1-bit bitmap)
    run_cmd("magick convert image.jpg -resize 2000x2000! org.pbm")
    run_cmd("magick convert org.pbm org.png")

    # 2. Extract header and body
    with open("org.pbm", "rb") as f:
        header = f.readline() + f.readline()
        body = f.read()

    with open("org.x", "wb") as f:
        f.write(body)

    print(f"Header: {header.strip()}")
    print(f"Body size: {len(body)} bytes")

    # 3. Encrypt with AES-256-ECB (no padding, no salt)
    run_cmd("openssl enc -aes-256-ecb -in org.x -nosalt -out enc.x -pass pass:1234 -nopad")
    run_cmd("copy /y enc.x enc_ecb.x")

    # 4. Encrypt with AES-256-CBC (comparing mode)
    run_cmd("openssl enc -aes-256-cbc -in org.x -nosalt -out enc_cbc.x -pass pass:1234 -iv 00000000000000000000000000000000 -nopad")

    # 5. Restore header for ECB
    with open("enc.x", "rb") as f:
        enc_ecb_data = f.read()
    with open("enc.pbm", "wb") as f:
        f.write(header + enc_ecb_data)
    with open("enc_ecb.pbm", "wb") as f:
        f.write(header + enc_ecb_data)
    run_cmd("magick convert enc_ecb.pbm enc_ecb.png")

    # 6. Restore header for CBC
    with open("enc_cbc.x", "rb") as f:
        enc_cbc_data = f.read()
    with open("enc_cbc.pbm", "wb") as f:
        f.write(header + enc_cbc_data)
    run_cmd("magick convert enc_cbc.pbm enc_cbc.png")

    print("[SUCCESS] All files generated successfully!")

if __name__ == "__main__":
    main()
