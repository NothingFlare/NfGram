/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

public class OpenH264Encoder extends WrappedNativeVideoEncoder {
  @Override
  public long createNativeVideoEncoder() {
    return nativeCreateEncoder();
  }

  static native long nativeCreateEncoder();

  @Override
  public boolean isHardwareEncoder() {
    return false;
  }
}
