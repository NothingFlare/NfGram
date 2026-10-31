/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * The FrameDecryptor interface allows Java API users to provide a
 * pointer to their native implementation of the FrameDecryptorInterface.
 * FrameDecryptors are extremely performance sensitive as they must process all
 * incoming video and audio frames. Due to this reason they should always be
 * backed by a native implementation
 * @note Not ready for production use.
 */
public interface FrameDecryptor {
  /**
   * @return A FrameDecryptorInterface pointer.
   */
  long getNativeFrameDecryptor();
}
