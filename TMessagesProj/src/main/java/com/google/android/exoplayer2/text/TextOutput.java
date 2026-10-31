/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import java.util.List;

/** Receives text output. */
public interface TextOutput {

  /**
   * Called when there is a change in the {@link Cue Cues}.
   *
   * <p>Both {@link #onCues(List)} and {@link #onCues(CueGroup)} are called when there is a change
   * in the cues. You should only implement one or the other.
   *
   * @deprecated Use {@link #onCues(CueGroup)} instead.
   */
  @Deprecated
  default void onCues(List<Cue> cues) {}

  /**
   * Called when there is a change in the {@link CueGroup}.
   *
   * <p>Both {@link #onCues(List)} and {@link #onCues(CueGroup)} are called when there is a change
   * in the cues. You should only implement one or the other.
   */
  void onCues(CueGroup cueGroup);
}
