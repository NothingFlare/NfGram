/*
 * Copyright (C) The WebRTC Project Authors. All rights reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import org.webrtc.CalledByNative;
import org.webrtc.Loggable;
import org.webrtc.Logging.Severity;

class JNILogging {
  private final Loggable loggable;

  public JNILogging(Loggable loggable) {
    this.loggable = loggable;
  }

  @CalledByNative
  public void logToInjectable(String message, Integer severity, String tag) {
    loggable.onLogMessage(message, Severity.values()[severity], tag);
  }
}
