package com.citizenzero.platform

import io.flutter.plugin.common.MethodChannel

class SecureEnclaveChannel(private val channel: MethodChannel) {
    fun setMethodCallHandler() {
        channel.setMethodCallHandler { call, result ->
            if (call.method == "generateKey") {
                // Call KeyStoreManager
                result.success(true)
            } else {
                result.notImplemented()
            }
        }
    }
}
