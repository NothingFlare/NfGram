/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

/** Factory for {@link TransferRtpDataChannel}. */
/* package */ final class TransferRtpDataChannelFactory implements RtpDataChannel.Factory {

  private static final int INTERLEAVED_CHANNELS_PER_TRACK = 2;

  private final long timeoutMs;

  /**
   * Creates a new instance.
   *
   * @param timeoutMs A positive number of milliseconds to wait before lack of received RTP packets
   *     is treated as the end of input.
   */
  public TransferRtpDataChannelFactory(long timeoutMs) {
    this.timeoutMs = timeoutMs;
  }

  @Override
  public RtpDataChannel createAndOpenDataChannel(int trackId) {
    TransferRtpDataChannel dataChannel = new TransferRtpDataChannel(timeoutMs);
    dataChannel.open(RtpUtils.getIncomingRtpDataSpec(trackId * INTERLEAVED_CHANNELS_PER_TRACK));
    return dataChannel;
  }
}
