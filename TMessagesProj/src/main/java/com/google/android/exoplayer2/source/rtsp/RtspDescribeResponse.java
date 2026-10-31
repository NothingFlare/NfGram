/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

/** Represents an RTSP DESCRIBE response. */
/* package */ final class RtspDescribeResponse {
  /** The response's status code. */
  public final int status;
  /** The {@link SessionDescription} (see RFC2327) in the DESCRIBE response. */
  public final SessionDescription sessionDescription;

  /**
   * Creates a new instance.
   *
   * @param status The response's status code.
   * @param sessionDescription The {@link SessionDescription} in the DESCRIBE response.
   */
  public RtspDescribeResponse(int status, SessionDescription sessionDescription) {
    this.status = status;
    this.sessionDescription = sessionDescription;
  }
}
