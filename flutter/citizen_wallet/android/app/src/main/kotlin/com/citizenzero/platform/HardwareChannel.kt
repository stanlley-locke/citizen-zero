package com.citizenzero.platform

import io.flutter.plugin.common.MethodChannel
import com.citizenzero.hardware.NFCManager
import com.citizenzero.hardware.BLEManager
import android.content.Context
import android.app.Activity

class HardwareChannel(
    private val channel: MethodChannel,
    private val context: Context,
    private val activity: Activity
) {
    private val nfcManager = NFCManager(context)
    // private val bleManager = BLEManager(context)

    fun setMethodCallHandler() {
        channel.setMethodCallHandler { call, result ->
            when (call.method) {
                "checkNfcAvailability" -> {
                    val supported = nfcManager.isNfcSupported()
                    val enabled = nfcManager.isNfcEnabled()
                    result.success(mapOf("supported" to supported, "enabled" to enabled))
                }
                "startNfcScan" -> {
                    // In a real app we'd hook up the ReaderCallback here
                    // For now, just confirming the call
                    result.success("Scanning started")
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }
}
