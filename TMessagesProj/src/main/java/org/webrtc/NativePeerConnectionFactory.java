/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Factory for creating webrtc::jni::OwnedPeerConnection instances. */
public interface NativePeerConnectionFactory {
  /**
   * Create a new webrtc::jni::OwnedPeerConnection instance and returns a pointer to it.
   * The caller takes ownership of the object.
   */
  long createNativePeerConnection();
}
