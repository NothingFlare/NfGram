/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata.scte35;

import com.google.android.exoplayer2.metadata.Metadata;

/** Superclass for SCTE35 splice commands. */
public abstract class SpliceCommand implements Metadata.Entry {

  @Override
  public String toString() {
    return "SCTE-35 splice command: type=" + getClass().getSimpleName();
  }

  // Parcelable implementation.

  @Override
  public int describeContents() {
    return 0;
  }
}
