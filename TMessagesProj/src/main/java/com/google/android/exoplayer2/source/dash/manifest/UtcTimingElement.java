/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.dash.manifest;

/** Represents a UTCTiming element. */
public final class UtcTimingElement {

  public final String schemeIdUri;
  public final String value;

  public UtcTimingElement(String schemeIdUri, String value) {
    this.schemeIdUri = schemeIdUri;
    this.value = value;
  }

  @Override
  public String toString() {
    return schemeIdUri + ", " + value;
  }
}
