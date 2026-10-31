/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * The FrameEncryptor interface allows Java API users to provide a pointer to
 * their native implementation of the FrameEncryptorInterface.
 * FrameEncyptors are extremely performance sensitive as they must process all
 * outgoing video and audio frames. Due to this reason they should always be
 * backed by a native implementation.
 * @note Not ready for production use.
 */
public interface FrameEncryptor {
  /**
   * @return A FrameEncryptorInterface pointer.
   */
  long getNativeFrameEncryptor();
}
