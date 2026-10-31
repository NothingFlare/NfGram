/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Factory for creating webrtc::NetworkStatePredictorFactory instances. */
public interface NetworkStatePredictorFactoryFactory {
  /**
   * Dynamically allocates a webrtc::NetworkStatePredictorFactory instance and returns a pointer to
   * it. The caller takes ownership of the object.
   */
  public long createNativeNetworkStatePredictorFactory();
}
