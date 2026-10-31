/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.ext.ffmpeg;

import com.google.android.exoplayer2.decoder.DecoderException;

/** Thrown when an FFmpeg decoder error occurs. */
public final class FfmpegDecoderException extends DecoderException {

  /* package */ FfmpegDecoderException(String message) {
    super(message);
  }

  /* package */ FfmpegDecoderException(String message, Throwable cause) {
    super(message, cause);
  }
}
