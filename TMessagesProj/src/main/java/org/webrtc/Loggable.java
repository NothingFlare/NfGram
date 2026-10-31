/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import org.webrtc.Logging.Severity;

/**
 * Java interface for WebRTC logging. The default implementation uses webrtc.Logging.
 *
 * When injected, the Loggable will receive logging from both Java and native.
 */
public interface Loggable {
  public void onLogMessage(String message, Severity severity, String tag);
}
