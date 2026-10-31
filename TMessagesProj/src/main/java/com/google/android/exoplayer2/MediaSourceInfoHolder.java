/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2;

import com.google.android.exoplayer2.source.MediaSource;

/** A holder of information about a {@link MediaSource}. */
/* package */ interface MediaSourceInfoHolder {

  /** Returns the uid of the {@link MediaSourceList.MediaSourceHolder}. */
  Object getUid();

  /** Returns the timeline. */
  Timeline getTimeline();
}
