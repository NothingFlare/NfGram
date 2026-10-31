/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Factory for creating webrtc::NetworkControllerFactory instances. */
public interface NetworkControllerFactoryFactory {
  /**
   * Dynamically allocates a webrtc::NetworkControllerFactory instance and returns a pointer to
   * it. The caller takes ownership of the object.
   */
  public long createNativeNetworkControllerFactory();
}
