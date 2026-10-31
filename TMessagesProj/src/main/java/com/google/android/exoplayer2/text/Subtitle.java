/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import com.google.android.exoplayer2.C;
import java.util.List;

/** A subtitle consisting of timed {@link Cue}s. */
public interface Subtitle {

  /**
   * Returns the index of the first event that occurs after a given time (exclusive).
   *
   * @param timeUs The time in microseconds.
   * @return The index of the next event, or {@link C#INDEX_UNSET} if there are no events after the
   *     specified time.
   */
  int getNextEventTimeIndex(long timeUs);

  /**
   * Returns the number of event times, where events are defined as points in time at which the cues
   * returned by {@link #getCues(long)} changes.
   *
   * @return The number of event times.
   */
  int getEventTimeCount();

  /**
   * Returns the event time at a specified index.
   *
   * @param index The index of the event time to obtain.
   * @return The event time in microseconds.
   */
  long getEventTime(int index);

  /**
   * Retrieve the cues that should be displayed at a given time.
   *
   * @param timeUs The time in microseconds.
   * @return A list of cues that should be displayed, possibly empty.
   */
  List<Cue> getCues(long timeUs);
}
