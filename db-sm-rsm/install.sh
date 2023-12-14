set -ve

apt-get update
apt-get install -y --no-install-recommends bison flex

export LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib
export LIBRARY_INCLUDE_PATH=/usr/local/include

# Install GMP-5.x library
wget https://src.fedoraproject.org/repo/pkgs/gmp/gmp-5.1.3.tar.bz2/a082867cbca5e898371a97bb27b31fea/gmp-5.1.3.tar.bz2
tar -xvjf gmp-5.1.3.tar.bz2
cd gmp-5.1.3
./configure --with-pic
make
make check
make install
cd ..
python3.7 -m pip install gmpy2


# Install PBC library
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvzf pbc-0.5.14.tar.gz
cd pbc-0.5.14
./configure
make
make install
cd ..

# Install OpenSSL (note: if your system already has openssl installed, do not execute the following steps)
wget https://www.openssl.org/source/openssl-3.2.0.tar.gz
tar -xvzf openssl-3.2.0.tar.gz
cd openssl-3.2.0
./Configure
make
make test
make install
cd ..

# Install Charm
git clone https://github.com/JHUISI/charm.git
cd charm
git checkout 6ac1d445fa0bd81b880c1a83accd8791acd2594b
./configure.sh
make