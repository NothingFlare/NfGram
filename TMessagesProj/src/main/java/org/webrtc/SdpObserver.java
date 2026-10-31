/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/** Interface for observing SDP-related events. */
public interface SdpObserver {
  /** Called on success of Create{Offer,Answer}(). */
  @CalledByNative void onCreateSuccess(SessionDescription sdp);

  /** Called on success of Set{Local,Remote}Description(). */
  @CalledByNative void onSetSuccess();

  /** Called on error of Create{Offer,Answer}(). */
  @CalledByNative void onCreateFailure(String error);

  /** Called on error of Set{Local,Remote}Description(). */
  @CalledByNative void onSetFailure(String error);
}
