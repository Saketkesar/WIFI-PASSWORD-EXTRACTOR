import subprocess
import re

# Summoning all saved WiFi profiles
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
profile_names = re.findall("All User Profile     : (.*)\r", command_output)

wifi_list = []

if profile_names:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        
        # Skip open networks
        if "Security key           : Absent" in profile_info:
            continue
        
        wifi_profile["ssid"] = name
        
        # Dig deeper (with key=clear) to expose passwords
        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
        password = re.search("Key Content            : (.*)\r", profile_info_pass)
        
        wifi_profile["password"] = password.group(1) if password else None
        wifi_list.append(wifi_profile)

# Print results and rethink your life
for wifi in wifi_list:
    print(wifi)
