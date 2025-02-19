

import os
import subprocess
import argparse
import sys
import shutil

# Constants
NUCLEI_BIN_PATH = os.path.expanduser("~/go/bin/nuclei")  # Default path after go install
TEMPLATES_DIR = os.path.expanduser("~/.nuclei-templates")

def setup_nuclei_templates():
    """Set up nuclei templates."""
    print("[*] Setting up nuclei templates...")
    if os.path.exists(TEMPLATES_DIR):
        print(f"[*] Templates directory already exists at {TEMPLATES_DIR}. Updating...")
        os.system(f"cd {TEMPLATES_DIR} && git pull")
    else:
        os.system(f"git clone https://github.com/projectdiscovery/nuclei-templates.git {TEMPLATES_DIR}")
    print(f"[+] Templates setup at {TEMPLATES_DIR}")

def run_nuclei_scan(target, cookies=None, templates=None):
    """Run nuclei scan on the target."""
    cmd = [NUCLEI_BIN_PATH, "-u", target]

    if cookies:
        cmd.extend(["-H", f"Cookie: {cookies}"])

    if templates:
        cmd.extend(["-t", templates])
    else:
        # Use default templates for http/exposure, time-based SQLi, XSS, CRLF, and open redirects
        cmd.extend(["-t", f"{TEMPLATES_DIR}/http/exposure.yaml"])
        cmd.extend(["-t", f"{TEMPLATES_DIR}/technologies/template-time-based-sqli.yaml"])
        cmd.extend(["-t", f"{TEMPLATES_DIR}/technologies/template-xss.yaml"])
        cmd.extend(["-t", f"{TEMPLATES_DIR}/technologies/template-crlf.yaml"])
        cmd.extend(["-t", f"{TEMPLATES_DIR}/technologies/template-open-redirect.yaml"])

    print(f"[*] Running nuclei scan on {target}...")
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Nuclei Wrapper for Web Application Security Testing")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan")
    parser.add_argument("-c", "--cookies", help="Cookies for authenticated testing (optional)")
    parser.add_argument("-t", "--templates", help="Path to custom nuclei templates (optional)")
    parser.add_argument("--setup-templates", action="store_true", help="Set up nuclei templates")

    args = parser.parse_args()

    if args.setup_templates:
        setup_nuclei_templates()
        sys.exit(0)

    if not shutil.which(NUCLEI_BIN_PATH):
        print("[-] nuclei is not installed. Please install it using:")
        print("    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")
        print("    Ensure ~/go/bin is in your PATH.")
        sys.exit(1)

    if not os.path.exists(TEMPLATES_DIR):
        print("[-] Nuclei templates are not set up. Please run with --setup-templates to set them up.")
        sys.exit(1)

    run_nuclei_scan(args.url, args.cookies, args.templates)

if __name__ == "__main__":
    main()


