/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.decoder;

import androidx.annotation.Nullable;

/** Thrown when a {@link Decoder} error occurs. */
public class DecoderException extends Exception {

  /**
   * Creates an instance.
   *
   * @param message The detail message for this exception.
   */
  public DecoderException(String message) {
    super(message);
  }

  /**
   * Creates an instance.
   *
   * @param cause The cause of this exception, or {@code null}.
   */
  public DecoderException(@Nullable Throwable cause) {
    super(cause);
  }

  /**
   * Creates an instance.
   *
   * @param message The detail message for this exception.
   * @param cause The cause of this exception, or {@code null}.
   */
  public DecoderException(String message, @Nullable Throwable cause) {
    super(message, cause);
  }
}
