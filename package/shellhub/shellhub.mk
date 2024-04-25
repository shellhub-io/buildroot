SHELLHUB_VERSION = 0.15.0
SHELLHUB_SITE = https://github.com/shellhub-io/shellhub/releases/download/v$(SHELLHUB_VERSION)
SHELLHUB_SOURCE = shellhub-agent.tar.gz
SHELLHUB_LICENSE = Apache-2.0
SHELLHUB_LICENSE_FILES = LICENSE.md
SHELLHUB_DEPENDENCIES = \
	libxcrypt \
	ca-certificates
SHELLHUB_GOMOD = github.com/shellhub-io/shellhub/agent
SHELLHUB_LDFLAGS = -X main.AgentVersion=v${SHELLHUB_VERSION}

define SHELLHUB_INSTALL_INIT_SYSTEMD
        $(INSTALL) -D -m 0644 $(SHELLHUB_PKGDIR)/shellhub.service \
                $(TARGET_DIR)/usr/lib/systemd/system/shellhub.service
endef

define SHELLHUB_INSTALL_INIT_SYSV
        $(INSTALL) -D -m 755 $(SHELLHUB_PKGDIR)/S42shellhub \
                $(TARGET_DIR)/etc/init.d/S42shellhub
endef

$(eval $(golang-package))
