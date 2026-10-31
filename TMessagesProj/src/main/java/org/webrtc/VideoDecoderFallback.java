/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * A combined video decoder that falls back on a secondary decoder if the primary decoder fails.
 */
public class VideoDecoderFallback extends WrappedNativeVideoDecoder {
  private final VideoDecoder fallback;
  private final VideoDecoder primary;

  public VideoDecoderFallback(VideoDecoder fallback, VideoDecoder primary) {
    this.fallback = fallback;
    this.primary = primary;
  }

  @Override
  public long createNativeVideoDecoder() {
    return nativeCreateDecoder(fallback, primary);
  }

  private static native long nativeCreateDecoder(VideoDecoder fallback, VideoDecoder primary);
}
