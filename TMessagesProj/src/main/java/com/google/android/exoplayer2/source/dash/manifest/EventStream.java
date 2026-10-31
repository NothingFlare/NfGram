/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.dash.manifest;

import com.google.android.exoplayer2.metadata.emsg.EventMessage;

/** A DASH in-MPD EventStream element, as defined by ISO/IEC 23009-1, 2nd edition, section 5.10. */
public final class EventStream {

  /** {@link EventMessage}s in the event stream. */
  public final EventMessage[] events;

  /** Presentation time of the events in microsecond, sorted in ascending order. */
  public final long[] presentationTimesUs;

  /** The scheme URI. */
  public final String schemeIdUri;

  /** The value of the event stream. Use empty string if not defined in manifest. */
  public final String value;

  /** The timescale in units per seconds, as defined in the manifest. */
  public final long timescale;

  public EventStream(
      String schemeIdUri,
      String value,
      long timescale,
      long[] presentationTimesUs,
      EventMessage[] events) {
    this.schemeIdUri = schemeIdUri;
    this.value = value;
    this.timescale = timescale;
    this.presentationTimesUs = presentationTimesUs;
    this.events = events;
  }

  /** A constructed id of this {@link EventStream}. Equal to {@code schemeIdUri + "/" + value}. */
  public String id() {
    return schemeIdUri + "/" + value;
  }
}
