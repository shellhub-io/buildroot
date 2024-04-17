# Buildroot external tree for ShellHub

This repository contains a Buildroot external tree for ShellHub.

# Usage

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

