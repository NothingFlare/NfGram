/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.effect;

import com.google.android.exoplayer2.util.FrameProcessingException;
import com.google.android.exoplayer2.util.GlUtil;

/**
 * Interface for tasks that may throw a {@link GlUtil.GlException} or {@link
 * FrameProcessingException}.
 */
/* package */ interface FrameProcessingTask {
  /** Runs the task. */
  void run() throws FrameProcessingException, GlUtil.GlException;
}
