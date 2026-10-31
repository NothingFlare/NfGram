/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import com.google.android.exoplayer2.PlaybackParameters;

/** Tracks the progression of media time. */
public interface MediaClock {

  /** Returns the current media position in microseconds. */
  long getPositionUs();

  /**
   * Attempts to set the playback parameters. The media clock may override the speed if changing the
   * playback parameters is not supported.
   *
   * @param playbackParameters The playback parameters to attempt to set.
   */
  void setPlaybackParameters(PlaybackParameters playbackParameters);

  /** Returns the active playback parameters. */
  PlaybackParameters getPlaybackParameters();
}
