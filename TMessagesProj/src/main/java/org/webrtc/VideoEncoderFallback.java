/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * A combined video encoder that falls back on a secondary encoder if the primary encoder fails.
 */
public class VideoEncoderFallback extends WrappedNativeVideoEncoder {
  private final VideoEncoder fallback;
  private final VideoEncoder primary;

  public VideoEncoderFallback(VideoEncoder fallback, VideoEncoder primary) {
    this.fallback = fallback;
    this.primary = primary;
  }

  @Override
  public long createNativeVideoEncoder() {
    return nativeCreateEncoder(fallback, primary);
  }

  @Override
  public boolean isHardwareEncoder() {
    return primary.isHardwareEncoder();
  }

  private static native long nativeCreateEncoder(VideoEncoder fallback, VideoEncoder primary);
}
