/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.ext.flac;

import com.google.android.exoplayer2.decoder.DecoderException;

/** Thrown when an Flac decoder error occurs. */
public final class FlacDecoderException extends DecoderException {

  /* package */ FlacDecoderException(String message) {
    super(message);
  }

  /* package */ FlacDecoderException(String message, Throwable cause) {
    super(message, cause);
  }
}
