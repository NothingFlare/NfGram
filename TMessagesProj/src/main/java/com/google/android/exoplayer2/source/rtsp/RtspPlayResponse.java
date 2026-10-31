/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

import com.google.common.collect.ImmutableList;
import java.util.List;

/** Represents an RTSP PLAY response. */
/* package */ final class RtspPlayResponse {
  /** The response's status code. */
  public final int status;
  /** The playback start timing, {@link RtspSessionTiming#DEFAULT} if not present. */
  public final RtspSessionTiming sessionTiming;
  /** The list of {@link RtspTrackTiming} representing the {@link RtspHeaders#RTP_INFO} header. */
  public final ImmutableList<RtspTrackTiming> trackTimingList;

  /**
   * Creates a new instance.
   *
   * @param status The response's status code.
   * @param sessionTiming The {@link RtspSessionTiming}, pass {@link RtspSessionTiming#DEFAULT} if
   *     not present.
   * @param trackTimingList The list of {@link RtspTrackTiming} representing the {@link
   *     RtspHeaders#RTP_INFO} header.
   */
  public RtspPlayResponse(
      int status, RtspSessionTiming sessionTiming, List<RtspTrackTiming> trackTimingList) {
    this.status = status;
    this.sessionTiming = sessionTiming;
    this.trackTimingList = ImmutableList.copyOf(trackTimingList);
  }
}
