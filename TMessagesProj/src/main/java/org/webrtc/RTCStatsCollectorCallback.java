/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Interface for receiving stats reports (see webrtc::RTCStatsCollectorCallback). */
public interface RTCStatsCollectorCallback {
  /** Called when the stats report is ready. */
  @CalledByNative public void onStatsDelivered(RTCStatsReport report);
}
