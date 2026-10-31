/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

/** Represents an RTSP Response. */
/* package */ final class RtspResponse {

  /** The status code of this response, as defined in RFC 2326 section 11. */
  public final int status;
  /** The headers of this response. */
  public final RtspHeaders headers;
  /** The body of this RTSP message, or empty string if absent. */
  public final String messageBody;

  /**
   * Creates a new instance.
   *
   * @param status The status code of this response, as defined in RFC 2326 section 11.
   * @param headers The headers of this response.
   * @param messageBody The body of this RTSP message, or empty string if absent.
   */
  public RtspResponse(int status, RtspHeaders headers, String messageBody) {
    this.status = status;
    this.headers = headers;
    this.messageBody = messageBody;
  }

  /**
   * Creates a new instance with an empty {@link #messageBody}.
   *
   * @param status The status code of this response, as defined in RFC 2326 section 11.
   * @param headers The headers of this response.
   */
  public RtspResponse(int status, RtspHeaders headers) {
    this(status, headers, /* messageBody= */ "");
  }
}
