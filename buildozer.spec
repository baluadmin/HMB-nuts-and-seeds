[app]
title = HMB Nuts & Spices
package.name = hmbnuts
package.domain = org.hmb
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,csv
version = 1.0
requirements = python3,kivy,pandas,requests,urllib3,certifi,idna,charset_normalizer
orientation = portrait
android.permissions = INTERNET
android.api = 31
android.minapi = 21

# Force stable NDK version to prevent compilation crash
android.ndk_version = 25b

android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_root = 1
