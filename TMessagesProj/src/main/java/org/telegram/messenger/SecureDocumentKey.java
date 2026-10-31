/*
 * Copyright (C) Nikolai Kudashov
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

public class SecureDocumentKey {

    public byte[] file_key;
    public byte[] file_iv;

    public SecureDocumentKey(byte[] key, byte[] iv) {
        file_key = key;
        file_iv = iv;
    }
}
