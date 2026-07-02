#!/bin/bash

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "Please run with sudo."
    exit 1
fi

echo "=== Raspberry Pi mDNS (Bonjour) Setup ==="
echo

read -rp "Enter a hostname (letters, numbers, hyphens only): " HOSTNAME

if [[ ! "$HOSTNAME" =~ ^[a-zA-Z0-9-]+$ ]]; then
    echo "Invalid hostname."
    exit 1
fi

echo
echo "Updating package lists..."
apt update

echo
echo "Installing Avahi..."
apt install -y avahi-daemon libnss-mdns

echo
echo "Setting hostname to '$HOSTNAME'..."
hostnamectl set-hostname "$HOSTNAME"

# Update /etc/hosts
CURRENT=$(hostname)

sed -i "s/^127\.0\.1\.1.*/127.0.1.1\t$HOSTNAME/" /etc/hosts

if ! grep -q "^127.0.1.1" /etc/hosts; then
    echo -e "127.0.1.1\t$HOSTNAME" >> /etc/hosts
fi

systemctl enable avahi-daemon
systemctl restart avahi-daemon

echo
echo "======================================="
echo "Setup complete!"
echo
echo "Hostname : $HOSTNAME"
echo "mDNS Name: $HOSTNAME.local"
echo
echo "From another Linux or macOS machine:"
echo
echo "    ssh $USER@$HOSTNAME.local"
echo
echo "or"
echo
echo "    ping $HOSTNAME.local"
echo
echo "A reboot isn't usually necessary, but if name resolution"
echo "doesn't work immediately, reboot the Pi."
