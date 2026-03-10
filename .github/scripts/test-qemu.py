#!/usr/bin/env python3
"""Boot a Buildroot QEMU image and validate the ShellHub agent installation."""

import sys
import os
import pexpect

TIMEOUT_BOOT = 180
TIMEOUT_CMD = 30
LOG_FILE = "/tmp/qemu-test.log"


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <images-dir>")
        sys.exit(1)

    images_dir = sys.argv[1]
    bzimage = os.path.join(images_dir, "bzImage")
    rootfs = os.path.join(images_dir, "rootfs.ext2")

    for path in (bzimage, rootfs):
        if not os.path.exists(path):
            print(f"ERROR: {path} not found")
            sys.exit(1)

    qemu_cmd = (
        f"qemu-system-x86_64"
        f" -M pc"
        f" -kernel {bzimage}"
        f" -drive file={rootfs},if=virtio,format=raw"
        f" -append \"rootwait root=/dev/vda console=ttyS0\""
        f" -nographic"
        f" -no-reboot"
    )

    print(f"Starting QEMU: {qemu_cmd}")
    logfile = open(LOG_FILE, "wb")
    child = pexpect.spawn(qemu_cmd, timeout=TIMEOUT_BOOT, logfile=logfile, encoding=None)

    tests_passed = 0
    tests_total = 3

    try:
        # Wait for login prompt
        print("Waiting for login prompt...")
        child.expect(b"login:", timeout=TIMEOUT_BOOT)
        child.sendline(b"root")

        # Wait for shell prompt
        child.expect(b"#", timeout=TIMEOUT_CMD)
        print("Logged in as root.")

        # Test 1: Binary exists and is executable
        print("Test 1: Checking binary exists...")
        child.sendline(b"test -x /usr/bin/shellhub-agent && echo TEST1_PASS || echo TEST1_FAIL")
        child.expect(b"TEST1_(PASS|FAIL)", timeout=TIMEOUT_CMD)
        if child.match.group(1) == b"PASS":
            print("  PASS: /usr/bin/shellhub-agent exists and is executable")
            tests_passed += 1
        else:
            print("  FAIL: /usr/bin/shellhub-agent not found or not executable")

        child.expect(b"#", timeout=TIMEOUT_CMD)

        # Test 2: Binary runs (--version or --help)
        print("Test 2: Checking binary runs...")
        child.sendline(b"shellhub-agent --version && echo TEST2_PASS || echo TEST2_FAIL")
        child.expect(b"TEST2_(PASS|FAIL)", timeout=TIMEOUT_CMD)
        if child.match.group(1) == b"PASS":
            print("  PASS: shellhub-agent --version works")
            tests_passed += 1
        else:
            print("  FAIL: shellhub-agent --version failed")

        child.expect(b"#", timeout=TIMEOUT_CMD)

        # Test 3: Init script installed
        print("Test 3: Checking init script...")
        child.sendline(b"test -f /etc/init.d/S42shellhub && echo TEST3_PASS || echo TEST3_FAIL")
        child.expect(b"TEST3_(PASS|FAIL)", timeout=TIMEOUT_CMD)
        if child.match.group(1) == b"PASS":
            print("  PASS: /etc/init.d/S42shellhub exists")
            tests_passed += 1
        else:
            print("  FAIL: /etc/init.d/S42shellhub not found")

        child.expect(b"#", timeout=TIMEOUT_CMD)

        # Shutdown
        print("Shutting down...")
        child.sendline(b"poweroff")
        child.expect(pexpect.EOF, timeout=60)

    except pexpect.TIMEOUT:
        print("ERROR: Timeout waiting for QEMU")
        child.close(force=True)
        logfile.close()
        sys.exit(1)
    except pexpect.EOF:
        print("ERROR: QEMU exited unexpectedly")
        logfile.close()
        sys.exit(1)

    logfile.close()

    print(f"\nResults: {tests_passed}/{tests_total} tests passed")
    if tests_passed < tests_total:
        sys.exit(1)

    print("All tests passed!")


if __name__ == "__main__":
    main()
