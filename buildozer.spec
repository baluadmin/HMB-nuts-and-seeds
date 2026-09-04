[app]

# (str) Title of your application
title = HMB Nuts & Spices

# (str) Package name
package.name = hmbnuts

# (str) Package domain (needed for android packaging)
package.domain = org.hmb

# (str) Source directory where the main file resides
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,csv

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,pandas,requests,urllib3,certifi,idna,charset_normalizer

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

[buildozer]
log_level = 2
warn_root = 1
