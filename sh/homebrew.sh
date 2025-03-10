#!/bin/bash

# 定义要安装的软件列表
software_list=(
    "squirrel"
    "hugo"
    "pyenv"
    "pyenv-virtualenv"
    "ffmpeg"
    "yt-dlp"
    "keka"
    "telegram"
    "spotify"
    "chatgpt"
    "easydict"
    "iina"
    "qbittorrent"
    "netnewswire"
    "shottr"
    "send-to-kindle"
    "rectangle"
    "foobar2000"
    "gpg-suite"
    "wechat"
    "hiddenbar"
    "obsidian"
    "font-ibm-plex-sans-sc"
    "font-ibm-plex-mono"
    "cherry-studio"
    "visual-studio-code"
    "app-cleaner"
    "teamviewer"
    "ollama"
    "zipic"
    "picgo"
)

# 逐个检查并安装软件
for package in "${software_list[@]}"; do
    echo "Checking if $package is installed..."
    # 从列表中提取包名
    package_name=$(echo "$package" | awk '{print $1}')
    
    if brew list "$package_name" &> /dev/null || brew list --versions "$package_name" &> /dev/null; then
        echo "$package_name is already installed. Skipping."
    else
        echo "Installing $package..."
        brew install $package
    fi
done

echo "All software installation completed."