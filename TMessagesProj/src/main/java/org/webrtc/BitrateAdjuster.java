/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Object that adjusts the bitrate of a hardware codec. */
interface BitrateAdjuster {
  /**
   * Sets the target bitrate in bits per second and framerate in frames per second.
   */
  void setTargets(int targetBitrateBps, int targetFps);

  /**
   * Should be used to report the size of an encoded frame to the bitrate adjuster. Use
   * getAdjustedBitrateBps to get the updated bitrate after calling this method.
   */
  void reportEncodedFrame(int size);

  /** Gets the current bitrate. */
  int getAdjustedBitrateBps();

  /** Gets the framerate for initial codec configuration. */
  int getCodecConfigFramerate();
}
