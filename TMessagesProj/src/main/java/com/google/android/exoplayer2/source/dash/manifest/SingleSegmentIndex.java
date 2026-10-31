/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.dash.manifest;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.source.dash.DashSegmentIndex;

/** A {@link DashSegmentIndex} that defines a single segment. */
/* package */ final class SingleSegmentIndex implements DashSegmentIndex {

  private final RangedUri uri;

  /**
   * @param uri A {@link RangedUri} defining the location of the segment data.
   */
  public SingleSegmentIndex(RangedUri uri) {
    this.uri = uri;
  }

  @Override
  public long getSegmentNum(long timeUs, long periodDurationUs) {
    return 0;
  }

  @Override
  public long getTimeUs(long segmentNum) {
    return 0;
  }

  @Override
  public long getDurationUs(long segmentNum, long periodDurationUs) {
    return periodDurationUs;
  }

  @Override
  public RangedUri getSegmentUrl(long segmentNum) {
    return uri;
  }

  @Override
  public long getFirstSegmentNum() {
    return 0;
  }

  @Override
  public long getFirstAvailableSegmentNum(long periodDurationUs, long nowUnixTimeUs) {
    return 0;
  }

  @Override
  public long getSegmentCount(long periodDurationUs) {
    return 1;
  }

  @Override
  public long getAvailableSegmentCount(long periodDurationUs, long nowUnixTimeUs) {
    return 1;
  }

  @Override
  public long getNextSegmentAvailableTimeUs(long periodDurationUs, long nowUnixTimeUs) {
    return C.TIME_UNSET;
  }

  @Override
  public boolean isExplicit() {
    return true;
  }
}
