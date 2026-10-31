/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.decoder.DecoderException;

/** Thrown when an error occurs decoding subtitle data. */
public class SubtitleDecoderException extends DecoderException {

  /**
   * @param message The detail message for this exception.
   */
  public SubtitleDecoderException(String message) {
    super(message);
  }

  /**
   * @param cause The cause of this exception, or {@code null}.
   */
  public SubtitleDecoderException(@Nullable Throwable cause) {
    super(cause);
  }

  /**
   * @param message The detail message for this exception.
   * @param cause The cause of this exception, or {@code null}.
   */
  public SubtitleDecoderException(String message, @Nullable Throwable cause) {
    super(message, cause);
  }
}
