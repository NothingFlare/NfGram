/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp;

import android.net.Uri;
import com.google.android.exoplayer2.upstream.DataSpec;
import com.google.android.exoplayer2.util.Util;

/** Utility methods for RTP. */
public final class RtpUtils {

  private static final String RTP_ANY_INCOMING_IPV4 = "rtp://0.0.0.0";

  /** Returns the {@link DataSpec} with the {@link Uri} for incoming RTP connection. */
  public static DataSpec getIncomingRtpDataSpec(int portNumber) {
    return new DataSpec(
        Uri.parse(Util.formatInvariant("%s:%d", RTP_ANY_INCOMING_IPV4, portNumber)));
  }

  private RtpUtils() {}
}
