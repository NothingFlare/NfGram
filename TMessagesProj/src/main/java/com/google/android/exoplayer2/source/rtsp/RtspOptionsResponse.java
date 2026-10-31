/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

import com.google.common.collect.ImmutableList;
import java.util.List;

/** Represents an RTSP OPTIONS response. */
/* package */ final class RtspOptionsResponse {
  /** The response's status code. */
  public final int status;
  /**
   * A list of methods supported by the RTSP server, encoded as {@link RtspRequest.Method}; or an
   * empty list if the server does not disclose the supported methods.
   */
  public final ImmutableList<Integer> supportedMethods;

  /**
   * Creates a new instance.
   *
   * @param status The response's status code.
   * @param supportedMethods A list of methods supported by the RTSP server, encoded as {@link
   *     RtspRequest.Method}; or an empty list if such information is not available.
   */
  public RtspOptionsResponse(int status, List<Integer> supportedMethods) {
    this.status = status;
    this.supportedMethods = ImmutableList.copyOf(supportedMethods);
  }
}
