/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.decoder;

/** Thrown when a non-platform component fails to decrypt data. */
public class CryptoException extends Exception {

  /** A component specific error code. */
  public final int errorCode;

  /**
   * @param errorCode A component specific error code.
   * @param message The detail message.
   */
  public CryptoException(int errorCode, String message) {
    super(message);
    this.errorCode = errorCode;
  }
}
