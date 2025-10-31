#!/usr/bin/python

import os
import random
from datetime import datetime

from . import googleplay_pb2, utils

GOOGLE_PUBKEY = "AAAAgMom/1a/v0lblO2Ubrt60J2gcuXSljGFQXgcyZWveWLEwo6prwgi3iJIZdodyhKZQrNWp5nKJ3srRXcUW+F1BD3baEVGcmEgqaLZUNBjm057pKRI16kB0YppeGx5qIQ5QjKzsR8ETQbKLNWgRY0QRNVz34kMJR3P/LgHax/6rmf5AAAAAwEAAQ=="

class DeviceBuilder(object):
    def __init__(self, device_codename):
        self.device_codename = device_codename
        self.locale = "en_US"
        self.timezone = "UTC"
        self.device = self.getDeviceProperties(device_codename)

    def setLocale(self, locale):
        self.locale = locale

    def setTimezone(self, timezone):
        self.timezone = timezone

    def getDeviceProperties(self, device_codename):
        """Get device properties from the device.properties file"""
        device = {}
        path = os.path.join(os.path.dirname(__file__), 'device.properties')
        current_section = None
        
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # Check for section header [device_name]
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    if current_section == device_codename:
                        continue
                
                # Parse properties in the matching section
                if current_section == device_codename and '=' in line:
                    key, value = line.split('=', 1)
                    device[key.strip()] = value.strip()
                
                # Stop when we reach another section after finding our device
                elif current_section == device_codename and line.startswith('['):
                    break
                    
        if not device:
            raise ValueError("Device codename not found: " + device_codename)
        return device

    def getBaseHeaders(self):
        return {
            "Accept-Language": self.locale,
            "Authorization": "GoogleLogin auth=",
            "X-DFE-Enabled-Experiments": "cl:billing.select_add_instrument_by_default",
            "X-DFE-Unsupported-Experiments": "nocache:billing.use_charging_poller,market_emails,buyer_currency,prod_baseline,checkin.set_asset_paid_app_field,shekel_test,content_ratings,buyer_currency_in_app,nocache:encrypted_apk,recent_changes",
            "X-DFE-Device-Id": self.device.get("Build.FINGERPRINT", ""),
            "X-DFE-Client-Id": "am-android-google",
            "User-Agent": self.getUserAgent(),
            "X-DFE-SmallestScreenWidthDp": "320",
            "X-DFE-Filter-Level": "3",
            "X-DFE-No-Prefetch": "true",
            "Accept-Encoding": "",
            "Host": "android.clients.google.com"
        }

    def getUserAgent(self):
        return "Android-Finsky/{} (api=3,versionCode={},sdk={},device={},hardware={},product={},model={},build={})".format(
            self.device.get("Vending.version", ""),
            self.device.get("Vending.versionCode", ""),
            self.device.get("Build.VERSION.SDK_INT", ""),
            self.device.get("Build.DEVICE", ""),
            self.device.get("Build.HARDWARE", ""),
            self.device.get("Build.PRODUCT", ""),
            self.device.get("Build.MODEL", ""),
            self.device.get("Build.ID", "")
        )

    def getDeviceUploadHeaders(self):
        headers = self.getBaseHeaders()
        headers["X-DFE-Enabled-Experiments"] = "cl:billing.select_add_instrument_by_default"
        headers["X-DFE-Unsupported-Experiments"] = "nocache:billing.use_charging_poller,market_emails,buyer_currency,prod_baseline,checkin.set_asset_paid_app_field,shekel_test,content_ratings,buyer_currency_in_app,nocache:encrypted_apk,recent_changes"
        headers["X-DFE-Device-Config-Token"] = ""
        headers["X-DFE-Device-Id"] = self.device.get("Build.FINGERPRINT", "")
        headers["X-DFE-Client-Id"] = "am-android-google"
        headers["X-DFE-SmallestScreenWidthDp"] = "320"
        headers["X-DFE-Filter-Level"] = "3"
        return headers

    def getAuthHeaders(self, gsfId=None):
        headers = {
            "User-Agent": "GoogleAuth/1.4 (bacon JDQ39)",
            "device": self.device.get("Build.DEVICE", ""),
            "app": "com.android.vending",
            "Accept-Encoding": "gzip"
        }
        if gsfId is not None:
            headers["X-DFE-Device-Id"] = "{0:x}".format(gsfId)
        return headers

    def getLoginParams(self, email, encrypted_password):
        return {
            "Email": email,
            "EncryptedPasswd": encrypted_password,
            "add_account": "1",
            "accountType": "HOSTED_OR_GOOGLE",
            "google_play_services_version": self.device.get("GSF.version", ""),
            "has_permission": "1",
            "source": "android",
            "device_country": self.locale.split('_')[1],
            "operatorCountry": self.locale.split('_')[1],
            "lang": self.locale.split('_')[0],
            "sdk_version": self.device.get("Build.VERSION.SDK_INT", "")
        }

    def getAndroidCheckinRequest(self):
        request = googleplay_pb2.AndroidCheckinRequest()
        request.id = 0
        request.checkin.CopyFrom(self.getAndroidCheckin())
        request.version = 3
        request.userSerialNumber = 0
        return request

    def getAndroidCheckin(self):
        checkin = googleplay_pb2.AndroidCheckinProto()
        checkin.build.CopyFrom(self.getBuild())
        checkin.lastCheckinMsec = 0
        checkin.cellOperator = self.device.get("CellOperator", "")
        checkin.simOperator = self.device.get("SimOperator", "")
        checkin.roaming = self.device.get("Roaming", "")
        checkin.userNumber = 0
        return checkin

    def getBuild(self):
        build = googleplay_pb2.AndroidBuildProto()
        build.id = self.device.get("Build.ID", "")
        build.product = self.device.get("Build.PRODUCT", "")
        build.carrier = self.device.get("Build.BRAND", "")
        build.radio = self.device.get("Build.RADIO", "")
        build.bootloader = self.device.get("Build.BOOTLOADER", "")
        build.device = self.device.get("Build.DEVICE", "")
        build.sdkVersion = int(self.device.get("Build.VERSION.SDK_INT", ""))
        build.model = self.device.get("Build.MODEL", "")
        build.manufacturer = self.device.get("Build.MANUFACTURER", "")
        build.buildProduct = self.device.get("Build.PRODUCT", "")
        build.client = "android-google"
        build.otaInstalled = False
        build.timestamp = int(datetime.now().timestamp() * 1000)
        build.googleServices = int(self.device.get("GSF.version", ""))
        return build

    def getDeviceConfig(self):
        config = googleplay_pb2.DeviceConfigurationProto()
        config.touchScreen = int(self.device.get("TouchScreen", ""))
        config.keyboard = int(self.device.get("Keyboard", ""))
        config.navigation = int(self.device.get("Navigation", ""))
        config.screenLayout = int(self.device.get("ScreenLayout", ""))
        config.hasHardKeyboard = self.device.get("HasHardKeyboard", "").lower() == "true"
        config.hasFiveWayNavigation = self.device.get("HasFiveWayNavigation", "").lower() == "true"
        config.screenDensity = int(self.device.get("ScreenDensity", ""))
        config.screenWidth = int(self.device.get("ScreenWidth", ""))
        config.screenHeight = int(self.device.get("ScreenHeight", ""))
        config.glEsVersion = int(self.device.get("GL.Version", ""))
        config.systemSharedLibrary.extend(self.device.get("SharedLibraries", "").split(","))
        config.systemAvailableFeature.extend(self.device.get("Features", "").split(","))
        config.nativePlatform.extend(self.device.get("Platforms", "").split(","))
        config.locale = self.locale
        config.glExtension.extend(self.device.get("GLExtensions", "").split(","))
        config.deviceClass = int(self.device.get("DeviceClass", ""))
        config.deviceSubclass = int(self.device.get("DeviceSubclass", ""))
        return config


def getDevicesCodenames():
    """Get all device codenames from the device.properties file"""
    devices = []
    path = os.path.join(os.path.dirname(__file__), 'device.properties')
    with open(path, 'r') as f:
        for line in f:
            if '=' in line:
                device_codename = line.split('=')[0].strip()
                devices.append(device_codename)
    return devices


def getDevicesReadableNames():
    """Get all device readable names from the device.properties file"""
    devices = {}
    path = os.path.join(os.path.dirname(__file__), 'device.properties')
    with open(path, 'r') as f:
        for line in f:
            if '=' in line:
                parts = line.split('=')
                device_codename = parts[0].strip()
                device_string = parts[1].strip()
                device_properties = device_string.split(',')
                for prop in device_properties:
                    if prop.startswith('Build.MODEL='):
                        model = prop.split('=')[1]
                        devices[device_codename] = model
                        break
    return devices