/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc.audio;

/**
 * This interface is a thin wrapper on top of a native C++ webrtc::AudioDeviceModule (ADM). The
 * reason for basing it on a native ADM instead of a pure Java interface is that we have two native
 * Android implementations (OpenSLES and AAudio) that does not make sense to wrap through JNI.
 *
 * <p>Note: This class is still under development and may change without notice.
 */
public interface AudioDeviceModule {
  /**
   * Returns a C++ pointer to a webrtc::AudioDeviceModule. Caller does _not_ take ownership and
   * lifetime is handled through the release() call.
   */
  long getNativeAudioDeviceModulePointer();

  /**
   * Release resources for this AudioDeviceModule, including native resources. The object should not
   * be used after this call.
   */
  void release();

  /** Control muting/unmuting the speaker. */
  void setSpeakerMute(boolean mute);

  /** Control muting/unmuting the microphone. */
  void setMicrophoneMute(boolean mute);
}
