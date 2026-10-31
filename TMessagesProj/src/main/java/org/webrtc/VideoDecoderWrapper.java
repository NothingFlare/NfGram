/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import org.webrtc.VideoDecoder;

/**
 * This class contains the Java glue code for JNI generation of VideoDecoder.
 */
class VideoDecoderWrapper {
  @CalledByNative
  static VideoDecoder.Callback createDecoderCallback(final long nativeDecoder) {
    return (VideoFrame frame, Integer decodeTimeMs,
               Integer qp) -> nativeOnDecodedFrame(nativeDecoder, frame, decodeTimeMs, qp);
  }

  private static native void nativeOnDecodedFrame(
      long nativeVideoDecoderWrapper, VideoFrame frame, Integer decodeTimeMs, Integer qp);
}
