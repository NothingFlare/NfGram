/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.rtsp.reader;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.util.Util;

/** Utility methods for {@link RtpPayloadReader}s. */
/* package */ class RtpReaderUtils {

  /**
   * Converts RTP timestamp and media frequency to sample presentation time, in microseconds
   *
   * @param startTimeOffsetUs The offset of the RTP timebase, in microseconds.
   * @param rtpTimestamp The RTP timestamp to convert.
   * @param firstReceivedRtpTimestamp The first received RTP timestamp.
   * @param mediaFrequency The media frequency.
   * @return The calculated sample presentation time, in microseconds.
   */
  public static long toSampleTimeUs(
      long startTimeOffsetUs,
      long rtpTimestamp,
      long firstReceivedRtpTimestamp,
      int mediaFrequency) {
    return startTimeOffsetUs
        + Util.scaleLargeTimestamp(
            rtpTimestamp - firstReceivedRtpTimestamp,
            /* multiplier= */ C.MICROS_PER_SECOND,
            /* divisor= */ mediaFrequency);
  }

  private RtpReaderUtils() {}
}
