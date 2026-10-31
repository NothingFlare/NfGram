/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Implementations of this interface can create a native {@code webrtc::NetEqFactory}.
 */
public interface NetEqFactoryFactory {
  /**
   * Returns a pointer to a {@code webrtc::NetEqFactory}. The caller takes ownership.
   */
  long createNativeNetEqFactory();
}
