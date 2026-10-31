/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.video;

import android.media.MediaCodec;
import android.view.Surface;
import androidx.annotation.Nullable;
import com.google.android.exoplayer2.mediacodec.MediaCodecDecoderException;
import com.google.android.exoplayer2.mediacodec.MediaCodecInfo;

/** Thrown when a failure occurs in a {@link MediaCodec} video decoder. */
public class MediaCodecVideoDecoderException extends MediaCodecDecoderException {

  /** The {@link System#identityHashCode(Object)} of the surface when the exception occurred. */
  public final int surfaceIdentityHashCode;

  /** Whether the surface was valid when the exception occurred. */
  public final boolean isSurfaceValid;

  public MediaCodecVideoDecoderException(
      Throwable cause, @Nullable MediaCodecInfo codecInfo, @Nullable Surface surface) {
    super(cause, codecInfo);
    surfaceIdentityHashCode = System.identityHashCode(surface);
    isSurfaceValid = surface == null || surface.isValid();
  }
}
