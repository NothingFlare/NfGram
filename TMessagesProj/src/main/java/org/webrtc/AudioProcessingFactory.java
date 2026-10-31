/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Factory for creating webrtc::AudioProcessing instances. */
public interface AudioProcessingFactory {
  /**
   * Dynamically allocates a webrtc::AudioProcessing instance and returns a pointer to it.
   * The caller takes ownership of the object.
   */
  public long createNative();
}
