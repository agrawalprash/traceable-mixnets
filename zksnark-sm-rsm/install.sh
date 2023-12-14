set -ve

# Install basic dependencies
apt-get update
apt-get install -y --no-install-recommends bison curl flex ca-certificates #python3-pip

# Install ZoKrates
curl -LSfs get.zokrat.es | sh

# Install bitstring
python3.7 -m pip install bitstring