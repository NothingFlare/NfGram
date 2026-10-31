/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Java wrapper for a C++ AudioSourceInterface.  Used as the source for one or
 * more {@code AudioTrack} objects.
 */
public class AudioSource extends MediaSource {
  public AudioSource(long nativeSource) {
    super(nativeSource);
  }

  /** Returns a pointer to webrtc::AudioSourceInterface. */
  long getNativeAudioSource() {
    return getNativeMediaSource();
  }
}
