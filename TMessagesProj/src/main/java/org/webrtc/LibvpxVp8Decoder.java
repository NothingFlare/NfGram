/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

public class LibvpxVp8Decoder extends WrappedNativeVideoDecoder {
  @Override
  public long createNativeVideoDecoder() {
    return nativeCreateDecoder();
  }

  static native long nativeCreateDecoder();
}
