package com.citizenzero.secure

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.PrivateKey

class KeyStoreManager {
    private val keyStore = KeyStore.getInstance("AndroidKeyStore").apply {
        load(null)
    }
    
    private val ASYMMETRIC_ALIAS = "CitizenZeroIdentityKey"

    fun generateIdentityKeyPair(): KeyPair {
        val keyPairGenerator = KeyPairGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_EC, 
            "AndroidKeyStore"
        )
        
        val parameterSpec = KeyGenParameterSpec.Builder(
            ASYMMETRIC_ALIAS,
            KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY
        )
            .setDigests(KeyProperties.DIGEST_SHA256, KeyProperties.DIGEST_SHA512)
            .setUserAuthenticationRequired(true) // Requires Biometric Auth to use key
            .setUserAuthenticationValidityDurationSeconds(30)
            .build()

        keyPairGenerator.initialize(parameterSpec)
        return keyPairGenerator.generateKeyPair()
    }

    fun signData(data: ByteArray): ByteArray {
        val privateKey = keyStore.getKey(ASYMMETRIC_ALIAS, null) as PrivateKey
        val signature = java.security.Signature.getInstance("SHA256withECDSA")
        signature.initSign(privateKey)
        signature.update(data)
        return signature.sign()
    }
    
    fun getPublicKey(): java.security.PublicKey? {
        val certificate = keyStore.getCertificate(ASYMMETRIC_ALIAS)
        return certificate?.publicKey
    }
}
