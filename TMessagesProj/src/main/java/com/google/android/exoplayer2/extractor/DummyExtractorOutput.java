/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor;

/** A fake {@link ExtractorOutput} implementation. */
public final class DummyExtractorOutput implements ExtractorOutput {

  @Override
  public TrackOutput track(int id, int type) {
    return new DummyTrackOutput();
  }

  @Override
  public void endTracks() {
    // Do nothing.
  }

  @Override
  public void seekMap(SeekMap seekMap) {
    // Do nothing.
  }
}
