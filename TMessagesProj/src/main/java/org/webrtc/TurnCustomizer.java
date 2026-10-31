/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Java wrapper for a C++ TurnCustomizer. */
public class TurnCustomizer {
  private long nativeTurnCustomizer;

  public TurnCustomizer(long nativeTurnCustomizer) {
    this.nativeTurnCustomizer = nativeTurnCustomizer;
  }

  public void dispose() {
    checkTurnCustomizerExists();
    nativeFreeTurnCustomizer(nativeTurnCustomizer);
    nativeTurnCustomizer = 0;
  }

  private static native void nativeFreeTurnCustomizer(long turnCustomizer);

  /** Return a pointer to webrtc::TurnCustomizer. */
  @CalledByNative
  long getNativeTurnCustomizer() {
    checkTurnCustomizerExists();
    return nativeTurnCustomizer;
  }

  private void checkTurnCustomizerExists() {
    if (nativeTurnCustomizer == 0) {
      throw new IllegalStateException("TurnCustomizer has been disposed.");
    }
  }
}
