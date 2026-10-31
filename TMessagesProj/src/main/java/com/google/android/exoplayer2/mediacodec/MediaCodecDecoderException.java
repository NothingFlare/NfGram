/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.mediacodec;

import android.media.MediaCodec;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import com.google.android.exoplayer2.decoder.DecoderException;
import com.google.android.exoplayer2.util.Util;

/** Thrown when a failure occurs in a {@link MediaCodec} decoder. */
public class MediaCodecDecoderException extends DecoderException {

  /** The {@link MediaCodecInfo} of the decoder that failed. Null if unknown. */
  @Nullable public final MediaCodecInfo codecInfo;

  /** An optional developer-readable diagnostic information string. May be null. */
  @Nullable public final String diagnosticInfo;

  public MediaCodecDecoderException(Throwable cause, @Nullable MediaCodecInfo codecInfo) {
    super("Decoder failed: " + (codecInfo == null ? null : codecInfo.name), cause);
    this.codecInfo = codecInfo;
    diagnosticInfo = Util.SDK_INT >= 21 ? getDiagnosticInfoV21(cause) : null;
  }

  @RequiresApi(21)
  @Nullable
  private static String getDiagnosticInfoV21(Throwable cause) {
    if (cause instanceof MediaCodec.CodecException) {
      return ((MediaCodec.CodecException) cause).getDiagnosticInfo();
    }
    return null;
  }
}
