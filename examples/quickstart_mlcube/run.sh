#!/bin/bash

set -e

# Cleanup
rm -rf mlcube clients/client_*

# Clone mlcube
git clone https://github.com/mlcommons/mlcube_examples.git && \
cp -r mlcube_examples/mnist_openfl mlcube && \
rm -rf mlcube_examples

# Build mlcube
pushd mlcube
poetry run mlcube_docker configure --mlcube=. --platform=platforms/docker.yaml
popd

# Start server
python server.py &
sleep 2 # Sleep for 2s to give the server enough time to start

for i in `seq 0 3`; do
    echo "Setting up client $i"
    mkdir -p clients/client_$i
    cp -r mlcube clients/client_$i/
    cp -r client.py clients/client_$i/
    python clients/client_$i/client.py &
done

# This will allow you to use CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
