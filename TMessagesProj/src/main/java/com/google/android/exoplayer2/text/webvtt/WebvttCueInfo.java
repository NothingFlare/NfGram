/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text.webvtt;

import com.google.android.exoplayer2.text.Cue;

/** A representation of a WebVTT cue. */
public final class WebvttCueInfo {

  public final Cue cue;
  public final long startTimeUs;
  public final long endTimeUs;

  public WebvttCueInfo(Cue cue, long startTimeUs, long endTimeUs) {
    this.cue = cue;
    this.startTimeUs = startTimeUs;
    this.endTimeUs = endTimeUs;
  }
}
