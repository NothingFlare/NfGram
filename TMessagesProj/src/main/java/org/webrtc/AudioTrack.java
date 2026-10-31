/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Java wrapper for a C++ AudioTrackInterface */
public class AudioTrack extends MediaStreamTrack {
  public AudioTrack(long nativeTrack) {
    super(nativeTrack);
  }

  /** Sets the volume for the underlying MediaSource. Volume is a gain value in the range
   *  0 to 10.
   */
  public void setVolume(double volume) {
    nativeSetVolume(getNativeAudioTrack(), volume);
  }

  /** Returns a pointer to webrtc::AudioTrackInterface. */
  long getNativeAudioTrack() {
    return getNativeMediaStreamTrack();
  }

  private static native void nativeSetVolume(long track, double volume);
}
