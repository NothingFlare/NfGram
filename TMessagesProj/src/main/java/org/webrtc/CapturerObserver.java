/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Interface for observering a capturer. Passed to {@link VideoCapturer#initialize}. Provided by
 * {@link VideoSource#getCapturerObserver}.
 *
 * All callbacks must be executed on a single thread.
 */
public interface CapturerObserver {
  /** Notify if the capturer have been started successfully or not. */
  void onCapturerStarted(boolean success);
  /** Notify that the capturer has been stopped. */
  void onCapturerStopped();

  /** Delivers a captured frame. */
  void onFrameCaptured(VideoFrame frame);
}
