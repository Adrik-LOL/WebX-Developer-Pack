#!/bin/bash

# Function to get the latest release information
get_latest_release() {
    repo_url="https://api.github.com/repos/face-hh/webx/releases/latest"
    curl -s "$repo_url" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

# Function to download the latest release
download_latest_release() {
    repo_name="face-hh/webx"
    latest_release=$(get_latest_release "$repo_name")
    if [ -n "$latest_release" ]; then
        download_url="https://github.com/$repo_name/archive/$latest_release.tar.gz"
        echo "Downloading latest release ($latest_release) from $download_url ..."
        # Download the release archive
        curl -LO "$download_url"
        # Extract the .neptune file from the archive
        tar -xzf "$latest_release.tar.gz" --wildcards --no-anchored '*.linux' --strip-components=1
        echo "Download complete."
        # Cleanup - Remove the downloaded archive
        rm "$latest_release.tar.gz"
    else
        echo "Failed to fetch the latest release."
    fi
}

download_latest_release
