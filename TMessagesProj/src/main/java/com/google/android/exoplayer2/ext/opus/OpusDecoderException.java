/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.ext.opus;

import com.google.android.exoplayer2.decoder.DecoderException;

/** Thrown when an Opus decoder error occurs. */
public final class OpusDecoderException extends DecoderException {

  /* package */ OpusDecoderException(String message) {
    super(message);
  }

  /* package */ OpusDecoderException(String message, Throwable cause) {
    super(message, cause);
  }
}
