/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import androidx.annotation.Nullable;

/** Factory for creating VideoDecoders. */
public interface VideoDecoderFactory {
  /**
   * Creates a VideoDecoder for the given codec. Supports the same codecs supported by
   * VideoEncoderFactory.
   */
  @Deprecated
  @Nullable
  default VideoDecoder createDecoder(String codecType) {
    throw new UnsupportedOperationException("Deprecated and not implemented.");
  }

  /** Creates a decoder for the given video codec. */
  @Nullable
  @CalledByNative
  default VideoDecoder createDecoder(VideoCodecInfo info) {
    return createDecoder(info.getName());
  }

  /**
   * Enumerates the list of supported video codecs.
   */
  @CalledByNative
  default VideoCodecInfo[] getSupportedCodecs() {
    return new VideoCodecInfo[0];
  }
}
