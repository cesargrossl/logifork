## Instalar vscode

sudo apt update && sudo apt install -y wget gpg

wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/microsoft.gpg > /dev/null

echo "Types: deb
URIs: https://packages.microsoft.com/repos/code
Suites: stable
Components: main
Architectures: amd64,arm64,armhf
Signed-By: /usr/share/keyrings/microsoft.gpg" \
  | sudo tee /etc/apt/sources.list.d/vscode.sources > /dev/null

sudo apt update && sudo apt install -y code


## 