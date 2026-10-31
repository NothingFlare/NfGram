/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Interface for observing Stats reports (see webrtc::StatsObservers). */
public interface StatsObserver {
  /** Called when the reports are ready.*/
  @CalledByNative public void onComplete(StatsReport[] reports);
}
