/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Factory for creating webrtc::FecControllerFactory instances.
 */
public interface FecControllerFactoryFactoryInterface {
  /**
   * Dynamically allocates a webrtc::FecControllerFactory instance and returns a pointer to it.
   * The caller takes ownership of the object.
   */
  public long createNative();
}
