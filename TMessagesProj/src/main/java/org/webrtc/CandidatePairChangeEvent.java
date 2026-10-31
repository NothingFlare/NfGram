/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Representation of a change in selected ICE candidate pair.
 * {@code CandidatePairChangeEvent} in the C++ API.
 */
public final class CandidatePairChangeEvent {
  public final IceCandidate local;
  public final IceCandidate remote;
  public final int lastDataReceivedMs;
  public final String reason;

  /**
   * An estimate from the ICE stack on how long it was disconnected before
   * changing to the new candidate pair in this event.
   * The first time an candidate pair is signaled the value will be 0.
   */
  public final int estimatedDisconnectedTimeMs;

  @CalledByNative
  CandidatePairChangeEvent(IceCandidate local, IceCandidate remote, int lastDataReceivedMs,
      String reason, int estimatedDisconnectedTimeMs) {
    this.local = local;
    this.remote = remote;
    this.lastDataReceivedMs = lastDataReceivedMs;
    this.reason = reason;
    this.estimatedDisconnectedTimeMs = estimatedDisconnectedTimeMs;
  }
}
