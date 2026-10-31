/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Implementations of this interface can create a native {@code webrtc::AudioDecoderFactory}.
 */
public interface AudioDecoderFactoryFactory {
  /**
   * Returns a pointer to a {@code webrtc::AudioDecoderFactory}. The caller takes ownership.
   */
  long createNativeAudioDecoderFactory();
}
