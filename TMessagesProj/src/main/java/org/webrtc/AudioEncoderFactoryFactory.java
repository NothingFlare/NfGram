/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Implementations of this interface can create a native {@code webrtc::AudioEncoderFactory}.
 */
public interface AudioEncoderFactoryFactory {
  /**
   * Returns a pointer to a {@code webrtc::AudioEncoderFactory}. The caller takes ownership.
   */
  long createNativeAudioEncoderFactory();
}
