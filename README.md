# Buildroot external tree for ShellHub

This repository contains a Buildroot external tree for ShellHub.

## Configuration

To configure the ShellHub agent on your Buildroot system,
you can use an overlay to add a custom configuration file
with the required environment variables.

Run the following command:

```
$ cat > rootfs_overlay/etc/default/shellhub-agent <<-EOF
SERVER_ADDRESS="https://your.shellhub.server.com"
PRIVATE_KEY="path_to_private_key_file"
TENANT_ID="your_tenant_id_here"
EOF
```

## Usage

Clone Buildroot:

```
$ git clone git://git.buildroot.net/buildroot
```

Clone this repository:

```
$ git clone https://github.com/shellhub-io/buildroot.git shellhub
```

Set the default configuration for emulated environment:

```
$ cd buildroot
$ make BR2_EXTERNAL=../shellhub qemu_x86_64_defconfig
```

Start the menuconfig and select `shellhub` under **External options**.

```
$ make BR2_EXTERNAL=../shellhub menuconfig
```

Finally run make to build everything.

```
$ make BR2_EXTERNAL=../shellhub rootfs-ext2
```

Start QEMU:

``` 
$ ./output/images/start-qemu.sh
```

