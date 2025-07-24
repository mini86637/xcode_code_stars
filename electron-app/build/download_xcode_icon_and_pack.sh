#!/bin/bash
# 自动下载Xcode图标并生成icns/ico，再自动打包Electron应用
set -e
cd "$(dirname "$0")"

ICON_PNG="icon.png"
ICON_ICNS="icon.icns"
ICON_ICO="icon.ico"

# 下载Xcode图标（Apple官方App Store图标，版权归Apple所有，仅供学习测试）
ICON_URL="https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/ce/39/a4/ce39a472-a515-e227-1c9e-3ce520212009/Xcode-85-220-0-4-0-0-2x-sRGB-0-0.png/1200x630bb.png"
if command -v wget >/dev/null 2>&1; then
  wget -O $ICON_PNG "$ICON_URL"
elif command -v curl >/dev/null 2>&1; then
  curl -L "$ICON_URL" -o $ICON_PNG
else
  echo "请手动下载 $ICON_URL 到 $ICON_PNG"; exit 1
fi


# 生成icns和ico（需安装 imagemagick 和 icnsutils/iconutil）
if command -v iconutil >/dev/null 2>&1; then
  mkdir -p icon.iconset
  if command -v convert >/dev/null 2>&1; then
    convert $ICON_PNG -resize 16x16   icon.iconset/icon_16x16.png
    convert $ICON_PNG -resize 32x32   icon.iconset/icon_32x32.png
    convert $ICON_PNG -resize 64x64   icon.iconset/icon_64x64.png
    convert $ICON_PNG -resize 128x128 icon.iconset/icon_128x128.png
    convert $ICON_PNG -resize 256x256 icon.iconset/icon_256x256.png
    convert $ICON_PNG -resize 512x512 icon.iconset/icon_512x512.png
  else
    sips -z 512 512 $ICON_PNG --out icon.iconset/icon_512x512.png || true
    sips -z 256 256 $ICON_PNG --out icon.iconset/icon_256x256.png || true
    sips -z 128 128 $ICON_PNG --out icon.iconset/icon_128x128.png || true
    sips -z 64 64 $ICON_PNG --out icon.iconset/icon_64x64.png || true
    sips -z 32 32 $ICON_PNG --out icon.iconset/icon_32x32.png || true
    sips -z 16 16 $ICON_PNG --out icon.iconset/icon_16x16.png || true
  fi
  iconutil -c icns icon.iconset -o $ICON_ICNS
  rm -rf icon.iconset
else
  echo "请手动将icon.png转换为icon.icns（macOS可用iconutil）"
fi

if command -v convert >/dev/null 2>&1; then
  convert $ICON_PNG -define icon:auto-resize=256,128,64,48,32,16 $ICON_ICO
else
  echo "请手动将icon.png转换为icon.ico（需imagemagick）"
fi

# 自动打包
cd ..
npm install
echo "开始打包..."
npm run dist
