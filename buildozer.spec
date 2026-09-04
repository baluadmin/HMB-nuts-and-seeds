[app]

# (str) Title of your application
title = HMB Nuts & Spices

# (str) Package name
package.name = hmbnuts

# (str) Package domain (needed for android packaging)
package.domain = org.hmb

# (list) Source files to include (let it include python and data files)
source.include_exts = py,png,jpg,kv,atlas,csv

# (list) Application requirements
# Note: python3, kivy, pandas, and requests are essential for your app logic
requirements = python3,kivy,pandas,requests,urllib3,certifi,idna,charset_normalizer,idna

# (str) Supported orientations (portrait keeps mobile layout clean)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
