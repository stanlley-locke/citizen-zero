package com.citizenzero.hardware

import android.content.Context
import android.nfc.NfcAdapter
import android.nfc.NfcManager
import android.os.Bundle

class NFCManager(private val context: Context) {
    private val nfcAdapter: NfcAdapter?

    init {
        val manager = context.getSystemService(Context.NFC_SERVICE) as NfcManager
        nfcAdapter = manager.defaultAdapter
    }

    fun isNfcSupported(): Boolean {
        return nfcAdapter != null
    }

    fun isNfcEnabled(): Boolean {
        return nfcAdapter?.isEnabled == true
    }

    fun enableReaderMode(activity: android.app.Activity, callback: NfcAdapter.ReaderCallback) {
        val options = Bundle()
        // Reduced polling delay for faster reading
        options.putInt(NfcAdapter.EXTRA_READER_PRESENCE_CHECK_DELAY, 250)
        
        nfcAdapter?.enableReaderMode(
            activity,
            callback,
            NfcAdapter.FLAG_READER_NFC_A or 
            NfcAdapter.FLAG_READER_NFC_B or 
            NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK,
            options
        )
    }

    fun disableReaderMode(activity: android.app.Activity) {
        nfcAdapter?.disableReaderMode(activity)
    }
}
