@echo off

REM Function to get the latest release information
:get_latest_release
set "repo_url=https://api.github.com/repos/face-hh/webx/releases/latest"
for /f "tokens=2 delims=:" %%a in ('curl -s "%repo_url%" ^| findstr /C:"\"tag_name\":"') do set "latest_release=%%~a"
set "latest_release=%latest_release:~2,-2%"

REM Function to download the latest release
:download_latest_release
set "repo_name=face-hh/webx"
if defined latest_release (
    set "download_url=https://github.com/%repo_name%/archive/%latest_release%.tar.gz"
    echo Downloading latest release (%latest_release%) from %download_url% ...
    curl -LO "%download_url%"
    REM Extract the .exe file from the archive
    tar -xzf "%latest_release%.tar.gz" --wildcards --no-anchored "*.exe" --strip-components=1
    echo Download complete.
    REM Cleanup - Remove the downloaded archive
    del "%latest_release%.tar.gz"
) else (
    echo Failed to fetch the latest release.
)
