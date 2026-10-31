/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

/** Represents an RTSP SETUP response. */
/* package */ final class RtspSetupResponse {

  /** The response's status code. */
  public final int status;
  /** The Session header (RFC2326 Section 12.37). */
  public final RtspMessageUtil.RtspSessionHeader sessionHeader;
  /** The Transport header (RFC2326 Section 12.39). */
  public final String transport;

  /**
   * Creates a new instance.
   *
   * @param status The response's status code.
   * @param sessionHeader The {@link RtspMessageUtil.RtspSessionHeader}.
   * @param transport The transport header included in the RTSP SETUP response.
   */
  public RtspSetupResponse(
      int status, RtspMessageUtil.RtspSessionHeader sessionHeader, String transport) {
    this.status = status;
    this.sessionHeader = sessionHeader;
    this.transport = transport;
  }
}
