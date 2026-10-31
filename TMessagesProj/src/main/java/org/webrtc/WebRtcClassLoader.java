/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * This class provides a ClassLoader that is capable of loading WebRTC Java classes regardless of
 * what thread it's called from. Such a ClassLoader is needed for the few cases where the JNI
 * mechanism is unable to automatically determine the appropriate ClassLoader instance.
 */
class WebRtcClassLoader {
  @CalledByNative
  static Object getClassLoader() {
    Object loader = WebRtcClassLoader.class.getClassLoader();
    if (loader == null) {
      throw new RuntimeException("Failed to get WebRTC class loader.");
    }
    return loader;
  }
}
