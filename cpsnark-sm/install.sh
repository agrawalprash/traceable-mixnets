set -ve

# Install basic dependencies
apt-get update
apt-get install -y --no-install-recommends bison curl flex ca-certificates build-essential

# Install Rust
curl https://sh.rustup.rs -sSf | bash -s -- -y
export PATH="$HOME/.cargo/bin:${PATH}"

# Install benchmark code
cargo build

# Run a dummy benchmark to fetch additional dependencies
cargo bench --no-run --bench membership_hash
